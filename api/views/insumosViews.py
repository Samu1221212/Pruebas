from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.db.models import F, Sum
from api.models.insumosModel import Insumo
from api.serializers.insumosSerializer import InsumoSerializer, InsumoDetailSerializer


class InsumoViewSet(viewsets.ModelViewSet):
    """
    ViewSet para manejar operaciones CRUD en Insumos.
    """
    queryset = Insumo.objects.all()
    serializer_class = InsumoSerializer
    
    def get_serializer_class(self):
        """
        Retorna el serializer apropiado dependiendo de la acción.
        """
        if self.action in ['retrieve', 'list']:
            return InsumoDetailSerializer
        return InsumoSerializer
    
    def get_queryset(self):
        """
        Opcionalmente filtra por estado, categoría o bajo stock.
        """
        queryset = Insumo.objects.all()
        estado = self.request.query_params.get('estado', None)
        categoria = self.request.query_params.get('categoria', None)
        nombre = self.request.query_params.get('nombre', None)
        bajo_stock = self.request.query_params.get('bajo_stock', None)
        
        if estado is not None:
            queryset = queryset.filter(estado=estado)
        
        if categoria is not None:
            queryset = queryset.filter(categoria_insumo_id=categoria)
            
        if nombre is not None:
            queryset = queryset.filter(nombre__icontains=nombre)
            
        if bajo_stock is not None and bajo_stock.lower() == 'true':
            queryset = queryset.filter(cantidad__lte=F('cantidad_minima'))
            
        return queryset
    
    @action(detail=False, methods=['get'])
    def activos(self, request):
        """
        Devuelve solo los insumos activos.
        """
        insumos = Insumo.objects.filter(estado='activo')
        serializer = InsumoDetailSerializer(insumos, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def bajo_stock(self, request):
        """
        Devuelve insumos con stock por debajo del mínimo.
        """
        insumos = Insumo.objects.filter(cantidad__lte=F('cantidad_minima'))
        serializer = InsumoDetailSerializer(insumos, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def por_categoria(self, request):
        """
        Agrupa insumos por categoría.
        """
        categoria_id = request.query_params.get('id', None)
        if categoria_id:
            insumos = Insumo.objects.filter(categoria_insumo_id=categoria_id)
            serializer = InsumoDetailSerializer(insumos, many=True)
            return Response(serializer.data)
        return Response({"error": "Se requiere el ID de la categoría"}, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['patch'])
    def cambiar_estado(self, request, pk=None):
        """
        Cambia el estado del insumo (activo/inactivo).
        """
        insumo = self.get_object()
        nuevo_estado = 'inactivo' if insumo.estado == 'activo' else 'activo'
        insumo.estado = nuevo_estado
        insumo.save()
        
        serializer = InsumoDetailSerializer(insumo)
        return Response(serializer.data)
    
    @action(detail=True, methods=['patch'])
    def ajustar_stock(self, request, pk=None):
        """
        Ajusta la cantidad de stock del insumo.
        """
        insumo = self.get_object()
        
        try:
            cantidad = int(request.data.get('cantidad', 0))
            if cantidad < 0 and abs(cantidad) > insumo.cantidad:
                return Response(
                    {"error": "No se puede reducir más de lo que hay en stock"}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            insumo.cantidad += cantidad
            insumo.save()
            
            serializer = InsumoDetailSerializer(insumo)
            return Response(serializer.data)
        except ValueError:
            return Response(
                {"error": "La cantidad debe ser un número entero"}, 
                status=status.HTTP_400_BAD_REQUEST
            )