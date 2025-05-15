from rest_framework import serializers
from api.models.insumosModel import Insumo
from api.models.categoriainsumoModel import CategoriaInsumo
from api.serializers.categoriainsumoSerializer import CategoriaInsumoSerializer

class InsumoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Insumo
        fields = '__all__'
        
    def validate_nombre(self, value):
        # Validar que el nombre no esté vacío
        if not value.strip():
            raise serializers.ValidationError("El nombre del insumo no puede estar vacío")
        return value
    
    def validate_precio(self, value):
        # Validar que el precio sea positivo
        if value <= 0:
            raise serializers.ValidationError("El precio debe ser mayor que cero")
        return value
    
    def validate_cantidad(self, value):
        # Validar que la cantidad no sea negativa
        if value < 0:
            raise serializers.ValidationError("La cantidad no puede ser negativa")
        return value


class InsumoDetailSerializer(serializers.ModelSerializer):
    categoria_insumo = CategoriaInsumoSerializer(read_only=True)
    
    class Meta:
        model = Insumo
        fields = '__all__'