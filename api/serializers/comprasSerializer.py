from rest_framework import serializers
from api.models.comprasModel import Compra
from api.models.comprahasinsumoModel import CompraHasInsumo
from api.models.proveedoresModel import Proveedor
from api.serializers.proveedoresSerializer import ProveedorSerializer
from api.serializers.insumosSerializer import InsumoSerializer
from api.serializers.comprahasinsumoSerializer import CompraHasInsumoSerializer, CompraHasInsumoDetailSerializer


class CompraSerializer(serializers.ModelSerializer):
    insumos = CompraHasInsumoSerializer(many=True, required=False, source='insumos')
    
    class Meta:
        model = Compra
        fields = ['id', 'estado', 'fecha_compra', 'total', 'proveedor', 'insumos', 'created_at', 'updated_at']
        read_only_fields = ['total']
        
    def validate_total(self, value):
        # Validar que el total sea positivo
        if value <= 0:
            raise serializers.ValidationError("El total debe ser mayor que cero")
        return value
    
    def create(self, validated_data):
        insumos_data = validated_data.pop('insumos', [])
        
        # Calcular el total de la compra
        total = sum(insumo_data['cantidad'] * insumo_data['precio_unitario'] for insumo_data in insumos_data)
        validated_data['total'] = total
        
        compra = Compra.objects.create(**validated_data)
        
        for insumo_data in insumos_data:
            insumo = insumo_data.get('insumo')
            cantidad = insumo_data.get('cantidad')
            precio_unitario = insumo_data.get('precio_unitario')
            subtotal = cantidad * precio_unitario
            
            from api.models.comprahasinsumoModel import CompraHasInsumo
            CompraHasInsumo.objects.create(
                compra=compra,
                insumo=insumo,
                cantidad=cantidad,
                precio_unitario=precio_unitario,
                subtotal=subtotal
            )
            
            # Actualizar el stock del insumo si la compra está completada
            if validated_data.get('estado') == 'completada':
                insumo.cantidad += cantidad
                insumo.save()
        
        return compra
    
    def update(self, instance, validated_data):
        insumos_data = validated_data.pop('insumos', None)
        
        # Revertir el stock si la compra estaba completada
        if instance.estado == 'completada' and validated_data.get('estado') != 'completada':
            for compra_insumo in instance.insumos.all():
                insumo = compra_insumo.insumo
                insumo.cantidad -= compra_insumo.cantidad
                insumo.save()
        
        if insumos_data is not None:
            # Calcular el nuevo total
            total = sum(insumo_data['cantidad'] * insumo_data['precio_unitario'] for insumo_data in insumos_data)
            validated_data['total'] = total
            
            # Eliminar los insumos anteriores
            instance.insumos.all().delete()
            
            # Crear los nuevos insumos
            for insumo_data in insumos_data:
                insumo = insumo_data.get('insumo')
                cantidad = insumo_data.get('cantidad')
                precio_unitario = insumo_data.get('precio_unitario')
                subtotal = cantidad * precio_unitario
                
                from api.models.comprahasinsumoModel import CompraHasInsumo
                CompraHasInsumo.objects.create(
                    compra=instance,
                    insumo=insumo,
                    cantidad=cantidad,
                    precio_unitario=precio_unitario,
                    subtotal=subtotal
                )
                
                # Actualizar el stock si la compra está completada
                if validated_data.get('estado', instance.estado) == 'completada':
                    insumo.cantidad += cantidad
                    insumo.save()
        
        # Actualizar el stock si el estado cambia a completada
        elif instance.estado != 'completada' and validated_data.get('estado') == 'completada':
            for compra_insumo in instance.insumos.all():
                insumo = compra_insumo.insumo
                insumo.cantidad += compra_insumo.cantidad
                insumo.save()
        
        return super().update(instance, validated_data)


class CompraDetailSerializer(serializers.ModelSerializer):
    proveedor = ProveedorSerializer(read_only=True)
    insumos = serializers.SerializerMethodField()
    
    class Meta:
        model = Compra
        fields = ['id', 'estado', 'fecha_compra', 'total', 'proveedor', 'insumos', 'created_at', 'updated_at']
    
    def get_insumos(self, obj):
        from api.models.comprahasinsumoModel import CompraHasInsumo
        compra_insumos = CompraHasInsumo.objects.filter(compra=obj)
        return CompraHasInsumoDetailSerializer(compra_insumos, many=True).data