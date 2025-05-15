from rest_framework import serializers
from django.db.models import F, Q
from api.models.agendamientocitasModel import AgendamientoCita
from api.models.clientesModel import Cliente
from api.models.manicuristasModel import Manicurista
from api.models.ventaserviciosModel import VentaServicio
from api.serializers.clientesSerializer import ClienteSerializer
from api.serializers.manicuristasSerializer import ManicuristaSerializer
from api.serializers.ventaserviciosSerializer import VentaServicioDetailSerializer

class AgendamientoCitaSerializer(serializers.ModelSerializer):
    class Meta:
        model = AgendamientoCita
        fields = '__all__'
        
    def validate(self, data):
        # Validar que la hora de salida sea posterior a la hora de entrada
        if data['hora_entrada'] >= data['hora_salida']:
            raise serializers.ValidationError("La hora de salida debe ser posterior a la hora de entrada")
        
        # Validar disponibilidad del manicurista
        manicurista = data['manicurista']
        hora_entrada = data['hora_entrada']
        hora_salida = data['hora_salida']
        
        # Buscar citas que se solapen con el mismo manicurista
        citas_solapadas = AgendamientoCita.objects.filter(
            manicurista=manicurista,
            estado__in=['pendiente', 'en_proceso'],
        ).filter(
            # Utilizando Q objects para crear condiciones OR correctamente
            Q(
                # La nueva cita comienza durante una cita existente
                hora_entrada__gte=F('hora_entrada'), 
                hora_entrada__lt=F('hora_salida')
            ) | 
            Q(
                # La nueva cita termina durante una cita existente
                hora_salida__gt=F('hora_entrada'), 
                hora_salida__lte=F('hora_salida')
            ) | 
            Q(
                # La nueva cita abarca completamente una cita existente
                hora_entrada__lte=F('hora_entrada'), 
                hora_salida__gte=F('hora_salida')
            )
        )
        
        # Excluir la cita actual en caso de actualización
        if self.instance:
            citas_solapadas = citas_solapadas.exclude(pk=self.instance.pk)
        
        if citas_solapadas.exists():
            raise serializers.ValidationError("El manicurista ya tiene una cita agendada en este horario")
        
        return data
    
    def create(self, validated_data):
        # Si el estado es finalizado, crear automáticamente una venta de servicio
        if validated_data.get('estado') == 'finalizado' and 'venta_servicio' not in validated_data:
            from api.models.serviciosModel import Servicio
            # Obtener el primer servicio disponible (esto debe ajustarse según tu lógica de negocio)
            servicio = Servicio.objects.filter(estado='activo').first()
            if servicio:
                venta = VentaServicio.objects.create(
                    total=servicio.precio,
                    cliente=validated_data['cliente'],
                    manicurista=validated_data['manicurista'],
                    servicio=servicio
                )
                validated_data['venta_servicio'] = venta
        
        return super().create(validated_data)
    
    def update(self, instance, validated_data):
        # Si el estado cambia a finalizado, crear automáticamente una venta de servicio
        if validated_data.get('estado') == 'finalizado' and instance.estado != 'finalizado' and not instance.venta_servicio:
            from api.models.serviciosModel import Servicio
            # Obtener el primer servicio disponible (esto debe ajustarse según tu lógica de negocio)
            servicio = Servicio.objects.filter(estado='activo').first()
            if servicio:
                venta = VentaServicio.objects.create(
                    total=servicio.precio,
                    cliente=instance.cliente,
                    manicurista=instance.manicurista,
                    servicio=servicio
                )
                validated_data['venta_servicio'] = venta
        
        return super().update(instance, validated_data)


class AgendamientoCitaDetailSerializer(serializers.ModelSerializer):
    cliente = ClienteSerializer(read_only=True)
    manicurista = ManicuristaSerializer(read_only=True)
    venta_servicio = VentaServicioDetailSerializer(read_only=True)
    
    class Meta:
        model = AgendamientoCita
        fields = '__all__'