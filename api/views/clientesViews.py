from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from api.models.clientesModel import Cliente
from api.serializers.clientesSerializer import ClienteSerializer


class ClienteViewSet(viewsets.ModelViewSet):
    """
    ViewSet para el modelo Cliente.
    Proporciona operaciones CRUD completas y algunos endpoints adicionales.
    """
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer
    
    @action(detail=False, methods=['get'])
    def by_documento(self, request):
        """
        Endpoint para buscar cliente por número de documento.
        """
        documento = request.query_params.get('documento')
        if not documento:
            return Response(
                {"error": "Se requiere el parámetro documento"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            cliente = self.get_queryset().get(documento=documento)
            serializer = self.get_serializer(cliente)
            return Response(serializer.data)
        except Cliente.DoesNotExist:
            return Response(
                {"error": "No se encontró el cliente con ese documento"}, 
                status=status.HTTP_404_NOT_FOUND
            )
    
    @action(detail=False, methods=['get'])
    def search(self, request):
        """
        Endpoint para buscar clientes por nombre o documento.
        """
        query = request.query_params.get('q', '')
        if not query:
            return Response(
                {"error": "Se requiere el parámetro q"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        clientes = self.get_queryset().filter(
            nombre__icontains=query
        ) | self.get_queryset().filter(
            documento__icontains=query
        )
        
        serializer = self.get_serializer(clientes, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def activos(self, request):
        """
        Endpoint para listar solo los clientes activos.
        """
        clientes = self.get_queryset().filter(estado='activo')
        serializer = self.get_serializer(clientes, many=True)
        return Response(serializer.data)