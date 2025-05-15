from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from api.models.serviciosModel import Servicio
from api.serializers.serviciosSerializer import ServicioSerializer


class ServicioViewSet(viewsets.ModelViewSet):
    """
    ViewSet para manejar operaciones CRUD en Servicios.
    """
    queryset = Servicio.objects.all()
    serializer_class = ServicioSerializer
    
    def get_queryset(self):
        """
        Opcionalmente filtra por estado o rango de precios.
        """
        queryset = Servicio.objects.all()
        estado = self.request.query_params.get('estado', None)
        precio_min = self.request.query_params.get('precio_min', None)
        precio_max = self.request.query_params.get('precio_max', None)
        nombre = self.request.query_params.get('nombre', None)
        
        if estado is not None:
            queryset = queryset.filter(estado=estado)
        
        if precio_min is not None:
            queryset = queryset.filter(precio__gte=precio_min)
            
        if precio_max is not None:
            queryset = queryset.filter(precio__lte=precio_max)
            
        if nombre is not None:
            queryset = queryset.filter(nombre__icontains=nombre)
            
        return queryset
    
    @action(detail=False, methods=['get'])
    def activos(self, request):
        """
        Devuelve solo los servicios activos.
        """
        servicios = Servicio.objects.filter(estado='activo')
        serializer = self.get_serializer(servicios, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def inactivos(self, request):
        """
        Devuelve solo los servicios inactivos.
        """
        servicios = Servicio.objects.filter(estado='inactivo')
        serializer = self.get_serializer(servicios, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['patch'])
    def cambiar_estado(self, request, pk=None):
        """
        Cambia el estado del servicio (activo/inactivo).
        """
        servicio = self.get_object()
        nuevo_estado = 'inactivo' if servicio.estado == 'activo' else 'activo'
        servicio.estado = nuevo_estado
        servicio.save()
        
        serializer = self.get_serializer(servicio)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def por_precio(self, request):
        """
        Ordena servicios por precio (ascendente o descendente).
        """
        orden = request.query_params.get('orden', 'asc')
        
        if orden.lower() == 'asc':
            servicios = Servicio.objects.all().order_by('precio')
        else:
            servicios = Servicio.objects.all().order_by('-precio')
            
        serializer = self.get_serializer(servicios, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def top_vendidos(self, request):
        """
        Devuelve los servicios más vendidos.
        """
        # Esta implementación dependerá de cómo están relacionados los modelos
        # Suponiendo que existe un modelo VentaServicio con una FK a Servicio
        from api.models.ventaserviciosModel import VentaServicio
        from django.db.models import Count
        
        limit = int(request.query_params.get('limit', 5))
        
        servicios_ids = VentaServicio.objects.values('servicio') \
            .annotate(total=Count('servicio')) \
            .order_by('-total')[:limit] \
            .values_list('servicio', flat=True)
        
        # Preservar el orden de la consulta anterior
        from django.db.models import Case, When, IntegerField
        order = Case(*[When(pk=pk, then=pos) for pos, pk in enumerate(servicios_ids)], 
                  output_field=IntegerField())
        
        servicios = Servicio.objects.filter(pk__in=servicios_ids).order_by(order)
        
        serializer = self.get_serializer(servicios, many=True)
        return Response(serializer.data)