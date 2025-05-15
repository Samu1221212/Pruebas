from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from django.contrib.auth.hashers import make_password
from random import randint
from datetime import timedelta

from api.serializers.solicitudcodigoSerializer import SolicitudCodigoSerializer
from api.serializers.confirmacioncodigoSerializer import ConfirmacionCodigoSerializer
from api.models.usuariosModel import Usuario
from api.models.codigorecuperacion import CodigoRecuperacion
from api.utils.email_utils import enviar_correo

class SolicitarCodigoRecuperacionView(APIView):
    def post(self, request):
        serializer = SolicitudCodigoSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        correo = serializer.validated_data['correo']
        usuario = Usuario.objects.get(correo=correo)

        codigo = f"{randint(100000, 999999)}"
        expiracion = timezone.now() + timedelta(minutes=10)

        CodigoRecuperacion.objects.update_or_create(
            usuario=usuario,
            defaults={
                'codigo': codigo,
                'creado_en': timezone.now(),
                'expiracion': expiracion
            }
        )

        asunto = "Código de recuperación de contraseña"
        mensaje = f"Tu código de recuperación es: {codigo}. Expira en 10 minutos."

        if enviar_correo(correo, asunto, mensaje):
            return Response({"mensaje": "Código enviado al correo."}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Error al enviar el correo."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ConfirmarCodigoRecuperacionView(APIView):
    def post(self, request):
        serializer = ConfirmacionCodigoSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        usuario = serializer.validated_data['usuario']
        nueva_password = request.data.get('nueva_password')
        registro = serializer.validated_data['registro']

        usuario.set_password(nueva_password)
        usuario.save()
        registro.delete()

        return Response({"mensaje": "Contraseña actualizada correctamente."}, status=status.HTTP_200_OK)
