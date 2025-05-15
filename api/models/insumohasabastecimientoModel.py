from django.db import models
from django.core.validators import MinValueValidator
from .base import BaseModel
from .insumosModel import Insumo
from .abastecimientosModel import Abastecimiento

class InsumoHasAbastecimiento(BaseModel):
    insumo = models.ForeignKey(Insumo, on_delete=models.PROTECT)
    abastecimiento = models.ForeignKey(Abastecimiento, on_delete=models.CASCADE, related_name='insumos')
    cantidad = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    
    def __str__(self):
        return f"{self.abastecimiento.id} - {self.insumo.nombre} ({self.cantidad})"
    
    class Meta:
        verbose_name = "Insumo - Abastecimiento"
        verbose_name_plural = "Insumos - Abastecimientos"