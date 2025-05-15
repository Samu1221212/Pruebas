# views/agendamientos/views.py
from rest_framework import viewsets, status, filters
from rest_framework.response import Response
from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend
from datetime import datetime, timedelta

from api.models.agendamientocitasModel import AgendamientoCita
from api.serializers.agendamientocitasSerializer import (
    AgendamientoCitaSerializer,
    AgendamientoCitaDetailSerializer
)


class AgendamientoCitaViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gestionar el ciclo completo de agendamiento de citas.
    
    Proporciona operaciones CRUD estándar y endpoints adicionales para
    filtrar citas por fecha, cliente, manicurista y estado.
    """
    queryset = AgendamientoCita.objects.all()
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['estado', 'cliente', 'manicurista', 'fecha']
    search_fields = ['cliente__nombre', 'cliente__apellido', 'manicurista__nombre', 'manicurista__apellido']
    ordering_fields = ['fecha', 'hora_entrada', 'estado']
    ordering = ['fecha', 'hora_entrada']
    
    def get_serializer_class(self):
        """
        Retorna el serializer apropiado según la acción
        - Para listar y recuperar detalle: AgendamientoCitaDetailSerializer
        - Para crear y actualizar: AgendamientoCitaSerializer
        """
        if self.action in ['list', 'retrieve']:
            return AgendamientoCitaDetailSerializer
        return AgendamientoCitaSerializer
    
    def perform_create(self, serializer):
        """
        Personaliza la creación de citas de agendamiento
        """
        serializer.save()
    
    @action(detail=False, methods=['get'])
    def hoy(self, request):
        """
        Endpoint para obtener las citas del día actual
        """
        fecha_hoy = datetime.now().date()
        citas = self.queryset.filter(fecha=fecha_hoy)
        serializer = AgendamientoCitaDetailSerializer(citas, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def semana(self, request):
        """
        Endpoint para obtener las citas de la semana actual
        """
        hoy = datetime.now().date()
        inicio_semana = hoy - timedelta(days=hoy.weekday())
        fin_semana = inicio_semana + timedelta(days=6)
        
        citas = self.queryset.filter(
            fecha__gte=inicio_semana,
            fecha__lte=fin_semana
        )
        serializer = AgendamientoCitaDetailSerializer(citas, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def pendientes(self, request):
        """
        Endpoint para obtener todas las citas pendientes
        """
        citas = self.queryset.filter(estado='pendiente')
        serializer = AgendamientoCitaDetailSerializer(citas, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['patch'])
    def cambiar_estado(self, request, pk=None):
        """
        Endpoint para cambiar el estado de una cita
        """
        cita = self.get_object()
        nuevo_estado = request.data.get('estado')
        
        if not nuevo_estado:
            return Response(
                {"error": "Se requiere el campo 'estado'"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Lista de estados válidos (ajustar según los estados en el modelo)
        estados_validos = ['pendiente', 'cancelado', 'en_proceso', 'finalizado']
        
        if nuevo_estado not in estados_validos:
            return Response(
                {"error": f"Estado no válido. Opciones: {', '.join(estados_validos)}"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        serializer = AgendamientoCitaSerializer(
            cita, 
            data={"estado": nuevo_estado}, 
            partial=True
        )
        
        if serializer.is_valid():
            serializer.save()
            # Devolvemos la representación detallada
            return Response(
                AgendamientoCitaDetailSerializer(cita).data,
                status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['get'])
    def por_manicurista(self, request):
        """
        Endpoint para filtrar citas por manicurista y fecha
        """
        manicurista_id = request.query_params.get('manicurista_id')
        fecha = request.query_params.get('fecha')
        
        if not manicurista_id:
            return Response(
                {"error": "Se requiere el parámetro 'manicurista_id'"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        citas = self.queryset.filter(manicurista_id=manicurista_id)
        
        if fecha:
            try:
                fecha_obj = datetime.strptime(fecha, '%Y-%m-%d').date()
                citas = citas.filter(fecha=fecha_obj)
            except ValueError:
                return Response(
                    {"error": "Formato de fecha inválido. Use YYYY-MM-DD"},
                    status=status.HTTP_400_BAD_REQUEST
                )
        
        serializer = AgendamientoCitaDetailSerializer(citas, many=True)
        return Response(serializer.data)