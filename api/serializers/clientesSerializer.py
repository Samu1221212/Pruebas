from rest_framework import serializers
from api.models.clientesModel import Cliente


class ClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = '__all__'
        
    def validate_nombre(self, value):
        # Validar que el nombre no esté vacío
        if not value.strip():
            raise serializers.ValidationError("El nombre no puede estar vacío")
        return value
    
    def validate_documento(self, value):
        # Validar que el documento no esté vacío
        if not value.strip():
            raise serializers.ValidationError("El documento no puede estar vacío")
        return value
    
    def validate_correo_electronico(self, value):
        # Validar que el correo electrónico tenga un formato válido
        if not value.strip():
            raise serializers.ValidationError("El correo electrónico no puede estar vacío")
        return value
