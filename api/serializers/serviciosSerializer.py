from rest_framework import serializers
from api.models.serviciosModel import Servicio


class ServicioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Servicio
        fields = '__all__'
        
    def validate_nombre(self, value):
        # Validar que el nombre no esté vacío
        if not value.strip():
            raise serializers.ValidationError("El nombre del servicio no puede estar vacío")
        return value
    
    def validate_precio(self, value):
        # Validar que el precio sea positivo
        if value <= 0:
            raise serializers.ValidationError("El precio debe ser mayor que cero")
        return value