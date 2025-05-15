from django.db import models
from django.core.validators import RegexValidator
from .base import BaseModel


class Cliente(BaseModel):
    TIPO_DOCUMENTO_CHOICES = (
        ('CC', 'Cédula de Ciudadanía'),
        ('CE', 'Cédula de Extranjería'),
        ('TI', 'Tarjeta de Identidad'),
        ('PP', 'Pasaporte'),
    )
    
    tipo_documento = models.CharField(max_length=2, choices=TIPO_DOCUMENTO_CHOICES)
    documento = models.CharField(max_length=20, unique=True)
    nombre = models.CharField(max_length=100)
    celular_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="El número de celular debe estar en formato: '+999999999'. Hasta 15 dígitos permitidos."
    )
    celular = models.CharField(validators=[celular_regex], max_length=15)
    correo_electronico = models.EmailField()
    direccion = models.CharField(max_length=200)
    
    def __str__(self):
        return f"{self.nombre} ({self.documento})"