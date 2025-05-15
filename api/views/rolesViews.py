from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from api.models.rolesModel import Rol, Permiso, RolHasPermiso
from api.serializers.rolesSerializer import (
    RolSerializer, 
    RolDetailSerializer,
    PermisoSerializer,
    RolHasPermisoSerializer
)


class RolViewSet(viewsets.ModelViewSet):
    """
    ViewSet para el modelo Rol.
    Proporciona operaciones CRUD completas y algunos endpoints adicionales.
    """
    queryset = Rol.objects.all()
    
    def get_serializer_class(self):
        """
        Retorna el serializer adecuado según la acción que se esté realizando.
        """
        if self.action == 'retrieve' or self.action == 'list_detail':
            return RolDetailSerializer
        return RolSerializer
    
    @action(detail=False, methods=['get'])
    def list_detail(self, request):
        """
        Endpoint para listar todos los roles con información detallada.
        """
        roles = self.get_queryset()
        serializer = self.get_serializer(roles, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def activos(self, request):
        """
        Endpoint para listar solo los roles activos.
        """
        roles = self.get_queryset().filter(estado='activo')
        serializer = self.get_serializer(roles, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def add_permiso(self, request, pk=None):
        """
        Endpoint para añadir un permiso a un rol.
        """
        rol = self.get_object()
        permiso_id = request.data.get('permiso_id')
        
        if not permiso_id:
            return Response(
                {"error": "Se requiere el parámetro permiso_id"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
            
        try:
            permiso = Permiso.objects.get(pk=permiso_id)
        except Permiso.DoesNotExist:
            return Response(
                {"error": "El permiso no existe"}, 
                status=status.HTTP_404_NOT_FOUND
            )
            
        # Verificar si ya existe la relación
        if RolHasPermiso.objects.filter(rol=rol, permiso=permiso).exists():
            return Response(
                {"error": "El rol ya tiene este permiso"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
            
        # Crear la relación
        RolHasPermiso.objects.create(rol=rol, permiso=permiso)
        
        return Response(
            {"mensaje": "Permiso añadido correctamente"}, 
            status=status.HTTP_201_CREATED
        )
    
    @action(detail=True, methods=['post'])
    def remove_permiso(self, request, pk=None):
        """
        Endpoint para eliminar un permiso de un rol.
        """
        rol = self.get_object()
        permiso_id = request.data.get('permiso_id')
        
        if not permiso_id:
            return Response(
                {"error": "Se requiere el parámetro permiso_id"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
            
        try:
            relacion = RolHasPermiso.objects.get(rol=rol, permiso_id=permiso_id)
            relacion.delete()
            return Response(
                {"mensaje": "Permiso eliminado correctamente"}, 
                status=status.HTTP_200_OK
            )
        except RolHasPermiso.DoesNotExist:
            return Response(
                {"error": "El rol no tiene este permiso"}, 
                status=status.HTTP_404_NOT_FOUND
            )


class PermisoViewSet(viewsets.ModelViewSet):
    """
    ViewSet para el modelo Permiso.
    Proporciona operaciones CRUD completas.
    """
    queryset = Permiso.objects.all()
    serializer_class = PermisoSerializer


class RolHasPermisoViewSet(viewsets.ModelViewSet):
    """
    ViewSet para el modelo RolHasPermiso.
    Proporciona operaciones CRUD completas y algunos endpoints adicionales.
    """
    queryset = RolHasPermiso.objects.all()
    serializer_class = RolHasPermisoSerializer
    
    @action(detail=False, methods=['get'])
    def by_rol(self, request):
        """
        Endpoint para filtrar por rol.
        """
        rol_id = request.query_params.get('rol_id')
        if not rol_id:
            return Response(
                {"error": "Se requiere el parámetro rol_id"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        relaciones = self.get_queryset().filter(rol_id=rol_id)
        serializer = self.get_serializer(relaciones, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def by_permiso(self, request):
        """
        Endpoint para filtrar por permiso.
        """
        permiso_id = request.query_params.get('permiso_id')
        if not permiso_id:
            return Response(
                {"error": "Se requiere el parámetro permiso_id"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        relaciones = self.get_queryset().filter(permiso_id=permiso_id)
        serializer = self.get_serializer(relaciones, many=True)
        return Response(serializer.data)