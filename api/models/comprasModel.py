from django.db import models
from django.core.validators import MinValueValidator
from .base import BaseModel
from .proveedoresModel import Proveedor

class Compra(BaseModel):
    ESTADO_CHOICES = (
        ('pendiente', 'Pendiente'),
        ('completada', 'Completada'),
        ('cancelada', 'Cancelada'),
    )
    
    estado = models.CharField(max_length=10, choices=ESTADO_CHOICES, default='pendiente')
    fecha_compra = models.DateField()
    total = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(0)])
    proveedor = models.ForeignKey(Proveedor, on_delete=models.PROTECT)
    
    def __str__(self):
        return f"Compra {self.id} - {self.proveedor.nombre_empresa} ({self.fecha_compra})"