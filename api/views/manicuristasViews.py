from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.db.models import Count, Sum
from api.models.manicuristasModel import Manicurista
from api.serializers.manicuristasSerializer import ManicuristaSerializer


class ManicuristaViewSet(viewsets.ModelViewSet):
    """
    ViewSet para manejar operaciones CRUD en Manicuristas.
    """
    queryset = Manicurista.objects.all()
    serializer_class = ManicuristaSerializer
    
    def get_queryset(self):
        """
        Opcionalmente filtra por estado o disponibilidad.
        """
        queryset = Manicurista.objects.all()
        estado = self.request.query_params.get('estado', None)
        disponible = self.request.query_params.get('disponible', None)
        
        if estado is not None:
            queryset = queryset.filter(estado=estado)
        
        if disponible is not None:
            disponible_bool = disponible.lower() == 'true'
            queryset = queryset.filter(disponible=disponible_bool)
            
        return queryset
    
    @action(detail=False, methods=['get'])
    def activos(self, request):
        """
        Devuelve solo los manicuristas activos.
        """
        manicuristas = Manicurista.objects.filter(estado='activo')
        serializer = self.get_serializer(manicuristas, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def disponibles(self, request):
        """
        Devuelve solo los manicuristas disponibles.
        """
        manicuristas = Manicurista.objects.filter(disponible=True, estado='activo')
        serializer = self.get_serializer(manicuristas, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['patch'])
    def cambiar_estado(self, request, pk=None):
        """
        Cambia el estado del manicurista (activo/inactivo).
        """
        manicurista = self.get_object()
        nuevo_estado = 'inactivo' if manicurista.estado == 'activo' else 'activo'
        manicurista.estado = nuevo_estado
        manicurista.save()
        
        serializer = self.get_serializer(manicurista)
        return Response(serializer.data)
    
    @action(detail=True, methods=['patch'])
    def cambiar_disponibilidad(self, request, pk=None):
        """
        Cambia la disponibilidad del manicurista.
        """
        manicurista = self.get_object()
        manicurista.disponible = not manicurista.disponible
        manicurista.save()
        
        serializer = self.get_serializer(manicurista)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def estadisticas(self, request, pk=None):
        """
        Devuelve estadísticas de servicios realizados por el manicurista.
        """
        manicurista = self.get_object()
        
        # Esta implementación dependerá de cómo están relacionados los modelos
        # Suponiendo que existe un modelo VentaServicio con una FK a Manicurista
        from api.models.ventaserviciosModel import VentaServicio
        
        # Total de servicios realizados
        total_servicios = VentaServicio.objects.filter(manicurista=manicurista).count()
        
        # Total facturado
        total_facturado = VentaServicio.objects.filter(manicurista=manicurista).aggregate(
            total=Sum('total')
        )['total'] or 0
        
        return Response({
            'total_servicios': total_servicios,
            'total_facturado': total_facturado,
        })