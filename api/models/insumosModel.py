from django.db import models
from django.core.validators import MinValueValidator
from .base import BaseModel
from .categoriainsumoModel import CategoriaInsumo


class Insumo(BaseModel):
    ESTADO_CHOICES = (
        ('activo', 'Activo'),
        ('inactivo', 'Inactivo'),
    )
    
    nombre = models.CharField(max_length=100)
    precio = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    cantidad = models.PositiveIntegerField(default=0)
    estado = models.CharField(max_length=10, choices=ESTADO_CHOICES, default='activo')
    categoria_insumo = models.ForeignKey(CategoriaInsumo, on_delete=models.PROTECT)
    
    def __str__(self):
        return f"{self.nombre} ({self.categoria_insumo.nombre})"