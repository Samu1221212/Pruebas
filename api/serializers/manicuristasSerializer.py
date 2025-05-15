from rest_framework import serializers
from api.models.manicuristasModel import Manicurista


class ManicuristaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Manicurista
        fields = '__all__'
        
    def validate_nombres(self, value):
        # Validar que el nombre no esté vacío
        if not value.strip():
            raise serializers.ValidationError("El nombre no puede estar vacío")
        return value
    
    def validate_apellidos(self, value):
        # Validar que los apellidos no estén vacíos
        if not value.strip():
            raise serializers.ValidationError("Los apellidos no pueden estar vacíos")
        return value
