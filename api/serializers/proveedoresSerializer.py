from rest_framework import serializers
from api.models.proveedoresModel import Proveedor


class ProveedorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Proveedor
        fields = '__all__'
        
    def validate_nombre_empresa(self, value):
        # Validar que el nombre de la empresa no esté vacío
        if not value.strip():
            raise serializers.ValidationError("El nombre de la empresa no puede estar vacío")
        return value
    
    def validate_nit(self, value):
        # Validar que el NIT no esté vacío
        if not value.strip():
            raise serializers.ValidationError("El NIT no puede estar vacío")
        return value
    
    def validate_nombre(self, value):
        # Validar que el nombre no esté vacío
        if not value.strip():
            raise serializers.ValidationError("El nombre no puede estar vacío")
        return value
    
    def validate_correo_electronico(self, value):
        # Validar que el correo electrónico tenga un formato válido
        if not value.strip():
            raise serializers.ValidationError("El correo electrónico no puede estar vacío")
        return value