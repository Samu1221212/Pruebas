from django.db import models
from django.core.validators import MinValueValidator
from .base import BaseModel
from .manicuristasModel import Manicurista
from .semanasModel import Semana


class Liquidacion(BaseModel):
    valor = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    bonificacion = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)], default=0)
    manicurista = models.ForeignKey(Manicurista, on_delete=models.PROTECT)
    semana = models.ForeignKey(Semana, on_delete=models.PROTECT)
    
    def __str__(self):
        return f"Liquidación {self.manicurista} - Semana {self.semana.numero_semana}"
    
    class Meta:
        unique_together = ('manicurista', 'semana')
        verbose_name = "Liquidación"
        verbose_name_plural = "Liquidaciones"