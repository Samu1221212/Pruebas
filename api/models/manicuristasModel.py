from django.db import models
from .base import BaseModel


class Manicurista(BaseModel):
    ESTADO_CHOICES = (
        ('activo', 'Activo'),
        ('inactivo', 'Inactivo'),
    )
    
    nombres = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=100)
    estado = models.CharField(max_length=10, choices=ESTADO_CHOICES, default='activo')
    
    def __str__(self):
        return f"{self.nombres} {self.apellidos}"