from rest_framework import serializers
from api.models.liquidacionesModel import Liquidacion
from api.models.manicuristasModel import Manicurista
from api.models.semanasModel import Semana
from api.serializers.manicuristasSerializer import ManicuristaSerializer
from api.serializers.semanasSerializer import SemanaSerializer


class LiquidacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Liquidacion
        fields = '__all__'
        
    def validate(self, data):
        # Validar que no exista una liquidación para la misma manicurista y semana
        if Liquidacion.objects.filter(manicurista=data['manicurista'], semana=data['semana']).exists():
            if self.instance:
                # Si es una actualización, verificar que no sea el mismo objeto
                if self.instance.manicurista == data['manicurista'] and self.instance.semana == data['semana']:
                    return data
            raise serializers.ValidationError("Ya existe una liquidación para esta manicurista en esta semana")
        
        # Validar que el valor y la bonificación sean positivos
        if data['valor'] < 0:
            raise serializers.ValidationError("El valor no puede ser negativo")
        if data['bonificacion'] < 0:
            raise serializers.ValidationError("La bonificación no puede ser negativa")
        
        return data


class LiquidacionDetailSerializer(serializers.ModelSerializer):
    manicurista = ManicuristaSerializer(read_only=True)
    semana = SemanaSerializer(read_only=True)
    
    class Meta:
        model = Liquidacion
        fields = '__all__'
