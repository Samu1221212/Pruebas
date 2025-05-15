from rest_framework import serializers
from api.models.novedadesModel import Novedad
from api.models.manicuristasModel import Manicurista
from api.serializers.manicuristasSerializer import ManicuristaSerializer


class NovedadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Novedad
        fields = '__all__'
        
    def validate(self, data):
        # Validar que la hora de salida sea posterior a la hora de entrada si existe
        if 'hora_salida' in data and data['hora_salida'] and data['hora_entrada'] > data['hora_salida']:
            raise serializers.ValidationError("La hora de salida debe ser posterior a la hora de entrada")
        return data


class NovedadDetailSerializer(serializers.ModelSerializer):
    manicurista = ManicuristaSerializer(read_only=True)
    
    class Meta:
        model = Novedad
        fields = '__all__'