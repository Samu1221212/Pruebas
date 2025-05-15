from datetime import timezone
from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from ..models.codigorecuperacion import CodigoRecuperacion
from ..models.usuariosModel import Usuario

class ConfirmacionCodigoSerializer(serializers.Serializer):
    correo = serializers.EmailField()
    codigo = serializers.CharField(max_length=6)
    nueva_password = serializers.CharField(write_only=True)

    def validate(self, data):
        correo = data.get('correo')
        codigo = data.get('codigo')
        nueva_password = data.get('nueva_password')

        try:
            usuario = Usuario.objects.get(correo=correo)
        except Usuario.DoesNotExist:
            raise serializers.ValidationError("Usuario no encontrado.")

        try:
            registro = CodigoRecuperacion.objects.get(usuario=usuario, codigo=codigo)
        except CodigoRecuperacion.DoesNotExist:
            raise serializers.ValidationError("Código inválido.")

        if registro.expiracion < timezone.now():
            raise serializers.ValidationError("El código ha expirado.")

        try:
            validate_password(nueva_password)
        except Exception as e:
            raise serializers.ValidationError({"nueva_password": list(e.messages)})

        data['usuario'] = usuario
        data['registro'] = registro
        return data
