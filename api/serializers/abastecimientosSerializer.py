from rest_framework import serializers
from api.models.abastecimientosModel import Abastecimiento
from api.models.manicuristasModel import Manicurista
from api.serializers.manicuristasSerializer import ManicuristaSerializer
from api.models.insumohasabastecimientoModel import InsumoHasAbastecimiento
from api.serializers.insumohasabastecimientoSerializer import (
    InsumoHasAbastecimientoSerializer,
    InsumoHasAbastecimientoDetailSerializer
)



class AbastecimientoSerializer(serializers.ModelSerializer):
    insumos = InsumoHasAbastecimientoSerializer(many=True, required=False)
    
    class Meta:
        model = Abastecimiento
        fields = ['id', 'fecha', 'cantidad', 'manicurista', 'insumos']
        
    def validate_cantidad(self, value):
        # Validar que la cantidad sea positiva
        if value <= 0:
            raise serializers.ValidationError("La cantidad debe ser mayor que cero")
        return value
    
    def create(self, validated_data):
        insumos_data = validated_data.pop('insumos', [])
        abastecimiento = Abastecimiento.objects.create(**validated_data)
        
        for insumo_data in insumos_data:
            InsumoHasAbastecimiento.objects.create(abastecimiento=abastecimiento, **insumo_data)
        
        return abastecimiento
    
    def update(self, instance, validated_data):
        insumos_data = validated_data.pop('insumos', None)
        instance = super().update(instance, validated_data)
        
        if insumos_data is not None:
            instance.insumos.all().delete()
            for insumo_data in insumos_data:
                InsumoHasAbastecimiento.objects.create(abastecimiento=instance, **insumo_data)
        
        return instance


class AbastecimientoDetailSerializer(serializers.ModelSerializer):
    manicurista = ManicuristaSerializer(read_only=True)
    insumos = serializers.SerializerMethodField()
    
    class Meta:
        model = Abastecimiento
        fields = ['id', 'fecha', 'cantidad', 'manicurista', 'insumos']
    
    def get_insumos(self, obj):
        abastecimiento_insumos = InsumoHasAbastecimiento.objects.filter(abastecimiento=obj)
        return InsumoHasAbastecimientoDetailSerializer(abastecimiento_insumos, many=True).data