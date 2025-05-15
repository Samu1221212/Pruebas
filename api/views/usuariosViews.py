from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from django.contrib.auth.hashers import make_password
from api.models.usuariosModel import Usuario
from api.serializers.usuariosSerializer import UsuarioSerializer, UsuarioDetailSerializer


class UsuarioViewSet(viewsets.ModelViewSet):
    """
    ViewSet para el modelo Usuario.
    Proporciona operaciones CRUD completas y algunos endpoints adicionales.
    """
    queryset = Usuario.objects.all()
    
    def get_serializer_class(self):
        """
        Retorna el serializer adecuado según la acción que se esté realizando.
        """
        if self.action == 'retrieve' or self.action == 'list_detail':
            return UsuarioDetailSerializer
        return UsuarioSerializer
    
    @action(detail=False, methods=['get'])
    def list_detail(self, request):
        """
        Endpoint para listar todos los usuarios con información detallada.
        """
        usuarios = self.get_queryset()
        serializer = self.get_serializer(usuarios, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def activos(self, request):
        """
        Endpoint para listar solo los usuarios activos.
        """
        usuarios = self.get_queryset().filter(is_active=True)
        serializer = self.get_serializer(usuarios, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def by_rol(self, request):
        """
        Endpoint para filtrar usuarios por rol.
        """
        rol_id = request.query_params.get('rol_id')
        if not rol_id:
            return Response(
                {"error": "Se requiere el parámetro rol_id"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        usuarios = self.get_queryset().filter(rol_id=rol_id)
        serializer = self.get_serializer(usuarios, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def cambiar_password(self, request, pk=None):
        """
        Endpoint para cambiar la contraseña de un usuario.
        """
        usuario = self.get_object()
        nueva_password = request.data.get('nueva_password')
        
        if not nueva_password:
            return Response(
                {"error": "Se requiere el parámetro nueva_password"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
            
        # Validar longitud mínima de la contraseña
        if len(nueva_password) < 8:
            return Response(
                {"error": "La contraseña debe tener al menos 8 caracteres"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
            
        usuario.password = make_password(nueva_password)
        usuario.save()
        
        return Response(
            {"mensaje": "Contraseña actualizada correctamente"}, 
            status=status.HTTP_200_OK
        )
    
    @action(detail=True, methods=['patch'])
    def activar(self, request, pk=None):
        """
        Endpoint para activar un usuario.
        """
        usuario = self.get_object()
        usuario.is_active = True
        usuario.save()
        
        return Response(
            {"mensaje": "Usuario activado correctamente"}, 
            status=status.HTTP_200_OK
        )
    
    @action(detail=True, methods=['patch'])
    def desactivar(self, request, pk=None):
        """
        Endpoint para desactivar un usuario.
        """
        usuario = self.get_object()
        usuario.is_active = False
        usuario.save()
        
        return Response(
            {"mensaje": "Usuario desactivado correctamente"}, 
            status=status.HTTP_200_OK
        )