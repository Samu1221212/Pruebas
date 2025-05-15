from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.db.models import Sum, Count, F
from django.utils import timezone
from api.models.ventaserviciosModel import VentaServicio
from api.serializers.ventaserviciosSerializer import VentaServicioSerializer, VentaServicioDetailSerializer


class VentaServicioViewSet(viewsets.ModelViewSet):
    """
    ViewSet para manejar operaciones CRUD en Ventas de Servicios.
    """
    queryset = VentaServicio.objects.all()
    serializer_class = VentaServicioSerializer
    
    def get_serializer_class(self):
        """
        Retorna el serializer apropiado dependiendo de la acción.
        """
        if self.action in ['retrieve', 'list']:
            return VentaServicioDetailSerializer
        return VentaServicioSerializer
    
    def get_queryset(self):
        """
        Opcionalmente filtra por cliente, manicurista, servicio o rango de fechas.
        """
        queryset = VentaServicio.objects.all()
        cliente_id = self.request.query_params.get('cliente', None)
        manicurista_id = self.request.query_params.get('manicurista', None)
        servicio_id = self.request.query_params.get('servicio', None)
        fecha_inicio = self.request.query_params.get('fecha_inicio', None)
        fecha_fin = self.request.query_params.get('fecha_fin', None)
        
        if cliente_id is not None:
            queryset = queryset.filter(cliente_id=cliente_id)
        
        if manicurista_id is not None:
            queryset = queryset.filter(manicurista_id=manicurista_id)
            
        if servicio_id is not None:
            queryset = queryset.filter(servicio_id=servicio_id)
            
        if fecha_inicio is not None:
            queryset = queryset.filter(fecha__gte=fecha_inicio)
            
        if fecha_fin is not None:
            queryset = queryset.filter(fecha__lte=fecha_fin)
            
        return queryset
    
    @action(detail=False, methods=['get'])
    def por_cliente(self, request):
        """
        Filtra ventas por cliente.
        """
        cliente_id = request.query_params.get('id', None)
        if cliente_id:
            ventas = VentaServicio.objects.filter(cliente_id=cliente_id)
            serializer = VentaServicioDetailSerializer(ventas, many=True)
            return Response(serializer.data)
        return Response({"error": "Se requiere el ID del cliente"}, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['get'])
    def por_manicurista(self, request):
        """
        Filtra ventas por manicurista.
        """
        manicurista_id = request.query_params.get('id', None)
        if manicurista_id:
            ventas = VentaServicio.objects.filter(manicurista_id=manicurista_id)
            serializer = VentaServicioDetailSerializer(ventas, many=True)
            return Response(serializer.data)
        return Response({"error": "Se requiere el ID del manicurista"}, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['get'])
    def por_servicio(self, request):
        """
        Filtra ventas por servicio.
        """
        servicio_id = request.query_params.get('id', None)
        if servicio_id:
            ventas = VentaServicio.objects.filter(servicio_id=servicio_id)
            serializer = VentaServicioDetailSerializer(ventas, many=True)
            return Response(serializer.data)
        return Response({"error": "Se requiere el ID del servicio"}, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['get'])
    def hoy(self, request):
        """
        Devuelve las ventas del día actual.
        """
        hoy = timezone.now().date()
        ventas = VentaServicio.objects.filter(fecha=hoy)
        serializer = VentaServicioDetailSerializer(ventas, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def resumen_periodo(self, request):
        """
        Devuelve un resumen de ventas para un período específico.
        """
        fecha_inicio = request.query_params.get('fecha_inicio', None)
        fecha_fin = request.query_params.get('fecha_fin', None)
        
        if not fecha_inicio or not fecha_fin:
            return Response(
                {"error": "Se requieren fecha de inicio y fecha final"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        ventas = VentaServicio.objects.filter(fecha__range=[fecha_inicio, fecha_fin])
        
        # Calcular estadísticas
        total_ventas = ventas.aggregate(total=Sum('total'))['total'] or 0
        cantidad_ventas = ventas.count()
        
        # Ventas por manicurista
        ventas_por_manicurista = ventas.values(
            'manicurista__id', 
            'manicurista__nombres', 
            'manicurista__apellidos'
        ).annotate(
            total_ventas=Sum('total'),
            cantidad_servicios=Count('id')
        ).order_by('-total_ventas')
        
        # Ventas por servicio
        ventas_por_servicio = ventas.values(
            'servicio__id', 
            'servicio__nombre'
        ).annotate(
            total_ventas=Sum('total'),
            cantidad=Count('id')
        ).order_by('-cantidad')
        
        return Response({
            'total_ventas': total_ventas,
            'cantidad_ventas': cantidad_ventas,
            'ventas_por_manicurista': ventas_por_manicurista,
            'ventas_por_servicio': ventas_por_servicio
        })