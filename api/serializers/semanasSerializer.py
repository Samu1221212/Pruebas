from rest_framework import serializers
from api.models.semanasModel import Semana


class SemanaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Semana
        fields = '__all__'
        
    def validate(self, data):
        # Validar que la fecha final sea posterior a la fecha inicial
        if data['fecha_inicio'] > data['fecha_final']:
            raise serializers.ValidationError("La fecha final debe ser posterior a la fecha inicial")
        
        # Validar que el número de semana sea único para el año
        year = data['fecha_inicio'].year
        if Semana.objects.filter(numero_semana=data['numero_semana'], fecha_inicio__year=year).exists():
            if self.instance:
                # Si es una actualización, verificar que no sea el mismo objeto
                instance_year = self.instance.fecha_inicio.year
                if year == instance_year and data['numero_semana'] == self.instance.numero_semana:
                    return data
            raise serializers.ValidationError(f"Ya existe una semana con el número {data['numero_semana']} para el año {year}")
        
        return data
