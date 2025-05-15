from rest_framework import serializers
from api.models.ventaserviciosModel import VentaServicio
from api.models.clientesModel import Cliente
from api.models.manicuristasModel import Manicurista
from api.models.serviciosModel import Servicio
from api.serializers.clientesSerializer import ClienteSerializer
from api.serializers.manicuristasSerializer import ManicuristaSerializer
from api.serializers.serviciosSerializer import ServicioSerializer


class VentaServicioSerializer(serializers.ModelSerializer):
    class Meta:
        model = VentaServicio
        fields = '__all__'
        
    def validate_total(self, value):
        # Validar que el total sea positivo
        if value <= 0:
            raise serializers.ValidationError("El total debe ser mayor que cero")
        return value


class VentaServicioDetailSerializer(serializers.ModelSerializer):
    cliente = ClienteSerializer(read_only=True)
    manicurista = ManicuristaSerializer(read_only=True)
    servicio = ServicioSerializer(read_only=True)
    
    class Meta:
        model = VentaServicio
        fields = '__all__'