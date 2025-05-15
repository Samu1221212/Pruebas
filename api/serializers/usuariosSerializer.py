from rest_framework import serializers
from api.models.usuariosModel import Usuario
from api.models.rolesModel import Rol
from api.serializers.rolesSerializer import RolSerializer


class UsuarioSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False)
    
    class Meta:
        model = Usuario
        fields = [
            'id', 'nombre', 'tipo_documento', 'documento', 'direccion', 
            'celular', 'correo_electronico', 'rol', 'is_active', 
            'is_staff', 'date_joined', 'password', 'created_at', 'updated_at'
        ]
        extra_kwargs = {
            'password': {'write_only': True},
            'is_staff': {'read_only': True},
        }
        
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
        # Validar que el correo electrónico no esté vacío
        if not value.strip():
            raise serializers.ValidationError("El correo electrónico no puede estar vacío")
        return value
    
    def create(self, validated_data):
        password = validated_data.pop('password', None)
        usuario = Usuario.objects.create(**validated_data)
        
        if password:
            usuario.set_password(password)
            usuario.save()
        
        return usuario
    
    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        usuario = super().update(instance, validated_data)
        
        if password:
            usuario.set_password(password)
            usuario.save()
        
        return usuario


class UsuarioDetailSerializer(serializers.ModelSerializer):
    rol = RolSerializer(read_only=True)
    
    class Meta:
        model = Usuario
        fields = [
            'id', 'nombre', 'tipo_documento', 'documento', 'direccion',
            'celular', 'correo_electronico', 'rol', 'is_active',
            'is_staff', 'date_joined', 'created_at', 'updated_at'
        ]
