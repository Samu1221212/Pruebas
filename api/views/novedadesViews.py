from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.utils import timezone
from api.models.novedadesModel import Novedad
from api.serializers.novedadesSerializer import NovedadSerializer, NovedadDetailSerializer


class NovedadViewSet(viewsets.ModelViewSet):
    """
    ViewSet para manejar operaciones CRUD en Novedades.
    """
    queryset = Novedad.objects.all()
    serializer_class = NovedadSerializer
    
    def get_serializer_class(self):
        """
        Retorna el serializer apropiado dependiendo de la acción.
        """
        if self.action in ['retrieve', 'list']:
            return NovedadDetailSerializer
        return NovedadSerializer
    
    def get_queryset(self):
        """
        Opcionalmente filtra por manicurista o rango de fechas.
        """
        queryset = Novedad.objects.all()
        manicurista_id = self.request.query_params.get('manicurista', None)
        fecha_inicio = self.request.query_params.get('fecha_inicio', None)
        fecha_fin = self.request.query_params.get('fecha_fin', None)
        tipo = self.request.query_params.get('tipo', None)
        
        if manicurista_id is not None:
            queryset = queryset.filter(manicurista_id=manicurista_id)
        
        if fecha_inicio is not None:
            queryset = queryset.filter(fecha__gte=fecha_inicio)
            
        if fecha_fin is not None:
            queryset = queryset.filter(fecha__lte=fecha_fin)
            
        if tipo is not None:
            queryset = queryset.filter(tipo=tipo)
            
        return queryset
    
    @action(detail=False, methods=['get'])
    def por_manicurista(self, request):
        """
        Filtra novedades por manicurista.
        """
        manicurista_id = request.query_params.get('id', None)
        if manicurista_id:
            novedades = Novedad.objects.filter(manicurista_id=manicurista_id)
            serializer = NovedadDetailSerializer(novedades, many=True)
            return Response(serializer.data)
        return Response({"error": "Se requiere el ID del manicurista"}, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['get'])
    def por_fecha(self, request):
        """
        Filtra novedades por fecha.
        """
        fecha = request.query_params.get('fecha', None)
        if fecha:
            novedades = Novedad.objects.filter(fecha=fecha)
            serializer = NovedadDetailSerializer(novedades, many=True)
            return Response(serializer.data)
        return Response({"error": "Se requiere la fecha"}, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['get'])
    def por_tipo(self, request):
        """
        Filtra novedades por tipo.
        """
        tipo = request.query_params.get('tipo', None)
        if tipo:
            novedades = Novedad.objects.filter(tipo=tipo)
            serializer = NovedadDetailSerializer(novedades, many=True)
            return Response(serializer.data)
        return Response({"error": "Se requiere el tipo de novedad"}, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['patch'])
    def registrar_salida(self, request, pk=None):
        """
        Registra la hora de salida para una novedad.
        """
        novedad = self.get_object()
        
        if novedad.hora_salida:
            return Response(
                {"error": "Esta novedad ya tiene registrada una hora de salida"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        novedad.hora_salida = timezone.now().time()
        novedad.save()
        
        serializer = NovedadDetailSerializer(novedad)
        return Response(serializer.data)