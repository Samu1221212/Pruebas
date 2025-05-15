from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from datetime import datetime, timedelta
from api.models.semanasModel import Semana
from api.serializers.semanasSerializer import SemanaSerializer


class SemanaViewSet(viewsets.ModelViewSet):
    """
    ViewSet para manejar operaciones CRUD en Semanas.
    """
    queryset = Semana.objects.all()
    serializer_class = SemanaSerializer
    
    def get_queryset(self):
        """
        Opcionalmente filtra por año o estado.
        """
        queryset = Semana.objects.all().order_by('-fecha_inicio')
        año = self.request.query_params.get('año', None)
        estado = self.request.query_params.get('estado', None)
        
        if año is not None:
            queryset = queryset.filter(fecha_inicio__year=año)
        
        if estado is not None:
            queryset = queryset.filter(estado=estado)
            
        return queryset
    
    @action(detail=False, methods=['get'])
    def activas(self, request):
        """
        Devuelve solo las semanas activas.
        """
        semanas = Semana.objects.filter(estado='activo').order_by('-fecha_inicio')
        serializer = self.get_serializer(semanas, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def actual(self, request):
        """
        Devuelve la semana actual según la fecha del sistema.
        """
        hoy = datetime.now().date()
        try:
            semana = Semana.objects.get(fecha_inicio__lte=hoy, fecha_final__gte=hoy)
            serializer = self.get_serializer(semana)
            return Response(serializer.data)
        except Semana.DoesNotExist:
            return Response(
                {"error": "No hay una semana configurada para la fecha actual"}, 
                status=status.HTTP_404_NOT_FOUND
            )
    
    @action(detail=False, methods=['get'])
    def por_año(self, request):
        """
        Filtra semanas por año.
        """
        año = request.query_params.get('año', None)
        if año:
            semanas = Semana.objects.filter(fecha_inicio__year=año).order_by('numero_semana')
            serializer = self.get_serializer(semanas, many=True)
            return Response(serializer.data)
        return Response({"error": "Se requiere el año"}, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['post'])
    def generar_semanas_año(self, request):
        """
        Genera automáticamente las semanas para un año completo.
        """
        año = request.data.get('año', None)
        if not año:
            return Response({"error": "Se requiere el año"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            año = int(año)
            # Verificar si ya existen semanas para este año
            if Semana.objects.filter(fecha_inicio__year=año).exists():
                return Response(
                    {"error": f"Ya existen semanas configuradas para el año {año}"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Generar semanas para todo el año
            semanas_creadas = []
            fecha_inicio = datetime(año, 1, 1).date()
            # Ajustar al primer lunes del año
            while fecha_inicio.weekday() != 0:  # 0 = lunes
                fecha_inicio += timedelta(days=1)
            
            for numero_semana in range(1, 53):  # Máximo 52 semanas en un año
                fecha_final = fecha_inicio + timedelta(days=6)  # Hasta el domingo
                
                # Si ya pasamos al siguiente año, terminamos
                if fecha_inicio.year > año:
                    break
                
                semana = Semana.objects.create(
                    numero_semana=numero_semana,
                    fecha_inicio=fecha_inicio,
                    fecha_final=fecha_final,
                    estado='activo'
                )
                semanas_creadas.append(semana)
                
                # Avanzar a la siguiente semana
                fecha_inicio = fecha_final + timedelta(days=1)
            
            serializer = self.get_serializer(semanas_creadas, many=True)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        except ValueError:
            return Response(
                {"error": "El año debe ser un número entero válido"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
    
    @action(detail=True, methods=['patch'])
    def cambiar_estado(self, request, pk=None):
        """
        Cambia el estado de la semana (activo/inactivo).
        """
        semana = self.get_object()
        nuevo_estado = 'inactivo' if semana.estado == 'activo' else 'activo'
        semana.estado = nuevo_estado
        semana.save()
        
        serializer = self.get_serializer(semana)
        return Response(serializer.data)