
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from django.db.models import Sum, F
from api.models.comprasModel import Compra
from api.serializers.comprasSerializer import CompraSerializer, CompraDetailSerializer


class CompraViewSet(viewsets.ModelViewSet):
    """
    ViewSet para el modelo Compra.
    Proporciona operaciones CRUD completas y algunos endpoints adicionales.
    """
    queryset = Compra.objects.all()
    
    def get_serializer_class(self):
        """
        Retorna el serializer adecuado según la acción que se esté realizando.
        """
        if self.action == 'retrieve' or self.action == 'list_detail':
            return CompraDetailSerializer
        return CompraSerializer
    
    @action(detail=False, methods=['get'])
    def list_detail(self, request):
        """
        Endpoint para listar todas las compras con información detallada.
        """
        compras = self.get_queryset()
        serializer = self.get_serializer(compras, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def by_estado(self, request):
        """
        Endpoint para filtrar compras por estado.
        """
        estado = request.query_params.get('estado')
        if not estado:
            return Response(
                {"error": "Se requiere el parámetro estado"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        compras = self.get_queryset().filter(estado=estado)
        serializer = self.get_serializer(compras, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def by_proveedor(self, request):
        """
        Endpoint para filtrar compras por proveedor.
        """
        proveedor_id = request.query_params.get('proveedor_id')
        if not proveedor_id:
            return Response(
                {"error": "Se requiere el parámetro proveedor_id"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        compras = self.get_queryset().filter(proveedor_id=proveedor_id)
        serializer = self.get_serializer(compras, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def by_fecha(self, request):
        """
        Endpoint para filtrar compras por rango de fechas.
        """
        fecha_inicio = request.query_params.get('fecha_inicio')
        fecha_fin = request.query_params.get('fecha_fin')
        
        if not fecha_inicio or not fecha_fin:
            return Response(
                {"error": "Se requieren los parámetros fecha_inicio y fecha_fin"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        compras = self.get_queryset().filter(
            fecha_compra__gte=fecha_inicio,
            fecha_compra__lte=fecha_fin
        )
        serializer = self.get_serializer(compras, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def total_by_proveedor(self, request):
        """
        Endpoint para obtener el total de compras agrupadas por proveedor.
        """
        total_por_proveedor = (
            Compra.objects
            .filter(estado='completada')
            .values('proveedor', 'proveedor__nombre_empresa')
            .annotate(total_compras=Sum('total'))
            .order_by('-total_compras')
        )
        
        return Response(total_por_proveedor)
