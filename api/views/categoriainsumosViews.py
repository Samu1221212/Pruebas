from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from api.models.categoriainsumoModel import CategoriaInsumo
from api.serializers.categoriainsumoSerializer import CategoriaInsumoSerializer


class CategoriaInsumoViewSet(viewsets.ModelViewSet):
    """
    ViewSet para manejar operaciones CRUD en Categorías de Insumos.
    """
    queryset = CategoriaInsumo.objects.all()
    serializer_class = CategoriaInsumoSerializer
    
    def get_queryset(self):
        """
        Opcionalmente filtra por estado activo o inactivo.
        """
        queryset = CategoriaInsumo.objects.all()
        estado = self.request.query_params.get('estado', None)
        nombre = self.request.query_params.get('nombre', None)
        
        if estado is not None:
            queryset = queryset.filter(estado=estado)
        
        if nombre is not None:
            queryset = queryset.filter(nombre__icontains=nombre)
            
        return queryset
    
    @action(detail=False, methods=['get'])
    def activas(self, request):
        """
        Devuelve solo las categorías activas.
        """
        categorias = CategoriaInsumo.objects.filter(estado='activo')
        serializer = self.get_serializer(categorias, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def inactivas(self, request):
        """
        Devuelve solo las categorías inactivas.
        """
        categorias = CategoriaInsumo.objects.filter(estado='inactivo')
        serializer = self.get_serializer(categorias, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['patch'])
    def cambiar_estado(self, request, pk=None):
        """
        Cambia el estado de la categoría (activo/inactivo).
        """
        categoria = self.get_object()
        nuevo_estado = 'inactivo' if categoria.estado == 'activo' else 'activo'
        categoria.estado = nuevo_estado
        categoria.save()
        
        serializer = self.get_serializer(categoria)
        return Response(serializer.data)