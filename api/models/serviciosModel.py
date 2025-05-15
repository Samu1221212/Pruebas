from django.db import models
from django.core.validators import MinValueValidator
from .base import BaseModel


class Servicio(BaseModel):
    ESTADO_CHOICES = (
        ('activo', 'Activo'),
        ('inactivo', 'Inactivo'),
    )
    
    nombre = models.CharField(max_length=100)
    precio = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    descripcion = models.TextField()
    estado = models.CharField(max_length=10, choices=ESTADO_CHOICES, default='activo')
    imagen = models.ImageField(upload_to='servicios/', null=True, blank=True)
    
    def __str__(self):
        return self.nombre