from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.db.models import Sum
from api.models.liquidacionesModel import Liquidacion
from api.serializers.liquidacionesSerializer import LiquidacionSerializer, LiquidacionDetailSerializer


class LiquidacionViewSet(viewsets.ModelViewSet):
    """
    ViewSet para manejar operaciones CRUD en Liquidaciones.
    """
    queryset = Liquidacion.objects.all()
    serializer_class = LiquidacionSerializer
    
    def get_serializer_class(self):
        """
        Retorna el serializer apropiado dependiendo de la acción.
        """
        if self.action in ['retrieve', 'list']:
            return LiquidacionDetailSerializer
        return LiquidacionSerializer
    
    def get_queryset(self):
        """
        Opcionalmente filtra por manicurista o semana.
        """
        queryset = Liquidacion.objects.all()
        manicurista_id = self.request.query_params.get('manicurista', None)
        semana_id = self.request.query_params.get('semana', None)
        estado = self.request.query_params.get('estado', None)
        
        if manicurista_id is not None:
            queryset = queryset.filter(manicurista_id=manicurista_id)
        
        if semana_id is not None:
            queryset = queryset.filter(semana_id=semana_id)
            
        if estado is not None:
            queryset = queryset.filter(estado=estado)
            
        return queryset
    
    @action(detail=False, methods=['get'])
    def por_manicurista(self, request):
        """
        Filtra liquidaciones por manicurista.
        """
        manicurista_id = request.query_params.get('id', None)
        if manicurista_id:
            liquidaciones = Liquidacion.objects.filter(manicurista_id=manicurista_id)
            serializer = LiquidacionDetailSerializer(liquidaciones, many=True)
            return Response(serializer.data)
        return Response({"error": "Se requiere el ID del manicurista"}, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['get'])
    def por_semana(self, request):
        """
        Filtra liquidaciones por semana.
        """
        semana_id = request.query_params.get('id', None)
        if semana_id:
            liquidaciones = Liquidacion.objects.filter(semana_id=semana_id)
            serializer = LiquidacionDetailSerializer(liquidaciones, many=True)
            return Response(serializer.data)
        return Response({"error": "Se requiere el ID de la semana"}, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['get'])
    def pendientes(self, request):
        """
        Devuelve liquidaciones con estado pendiente.
        """
        liquidaciones = Liquidacion.objects.filter(estado='pendiente')
        serializer = LiquidacionDetailSerializer(liquidaciones, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def pagadas(self, request):
        """
        Devuelve liquidaciones con estado pagado.
        """
        liquidaciones = Liquidacion.objects.filter(estado='pagado')
        serializer = LiquidacionDetailSerializer(liquidaciones, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['patch'])
    def marcar_como_pagada(self, request, pk=None):
        """
        Marca una liquidación como pagada.
        """
        liquidacion = self.get_object()
        
        if liquidacion.estado == 'pagado':
            return Response(
                {"error": "Esta liquidación ya ha sido pagada"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        liquidacion.estado = 'pagado'
        liquidacion.save()
        
        serializer = LiquidacionDetailSerializer(liquidacion)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def resumen_semana(self, request):
        """
        Devuelve un resumen de las liquidaciones por semana.
        """
        semana_id = request.query_params.get('semana', None)
        if not semana_id:
            return Response({"error": "Se requiere el ID de la semana"}, status=status.HTTP_400_BAD_REQUEST)
        
        liquidaciones = Liquidacion.objects.filter(semana_id=semana_id)
        
        # Cálculos de resumen
        total_pagado = liquidaciones.filter(estado='pagado').aggregate(
            total=Sum('valor') + Sum('bonificacion')
        )['total'] or 0
        
        total_pendiente = liquidaciones.filter(estado='pendiente').aggregate(
            total=Sum('valor') + Sum('bonificacion')
        )['total'] or 0
        
        total_general = total_pagado + total_pendiente
        
        # Contar liquidaciones por estado
        pagadas_count = liquidaciones.filter(estado='pagado').count()
        pendientes_count = liquidaciones.filter(estado='pendiente').count()
        
        return Response({
            'total_pagado': total_pagado,
            'total_pendiente': total_pendiente,
            'total_general': total_general,
            'liquidaciones_pagadas': pagadas_count,
            'liquidaciones_pendientes': pendientes_count,
            'total_liquidaciones': pagadas_count + pendientes_count
        })
    
    @action(detail=False, methods=['post'])
    def generar_liquidaciones_semana(self, request):
        """
        Genera automáticamente las liquidaciones para todos los manicuristas en una semana.
        """
        semana_id = request.data.get('semana', None)
        if not semana_id:
            return Response({"error": "Se requiere el ID de la semana"}, status=status.HTTP_400_BAD_REQUEST)
        
        # Verificar si la semana existe
        from api.models.semanasModel import Semana
        try:
            semana = Semana.objects.get(pk=semana_id)
        except Semana.DoesNotExist:
            return Response({"error": "La semana especificada no existe"}, status=status.HTTP_404_NOT_FOUND)
        
        # Obtener todos los manicuristas activos
        from api.models.manicuristasModel import Manicurista
        manicuristas = Manicurista.objects.filter(estado='activo')
        
        liquidaciones_creadas = []
        for manicurista in manicuristas:
            # Verificar si ya existe una liquidación para este manicurista en esta semana
            if Liquidacion.objects.filter(manicurista=manicurista, semana=semana).exists():
                continue
                
            # Calcular valor y bonificación basado en ventas (implementación simplificada)
            # En un caso real, esto podría ser más complejo dependiendo de tu lógica de negocio
            from api.models.ventaserviciosModel import VentaServicio
            ventas = VentaServicio.objects.filter(
                manicurista=manicurista,
                fecha__range=(semana.fecha_inicio, semana.fecha_final)
            )
            
            total_ventas = ventas.aggregate(total=Sum('total'))['total'] or 0
            
            # Suponiendo que la manicurista recibe un porcentaje de las ventas
            valor = total_ventas * 0.5  # 50% del total de ventas
            
            # Bonificación basada en algún criterio
            bonificacion = 0
            if total_ventas > 1000000:  # Ejemplo: bono por ventas altas
                bonificacion = 50000
            
            liquidacion = Liquidacion.objects.create(
                manicurista=manicurista,
                semana=semana,
                valor=valor,
                bonificacion=bonificacion,
                estado='pendiente'
            )
            liquidaciones_creadas.append(liquidacion)
        
        serializer = LiquidacionDetailSerializer(liquidaciones_creadas, many=True)
        return Response(serializer.data, status=status.HTTP_201_CREATED)