from django.db import models
from .base import BaseModel


class Semana(BaseModel):
    numero_semana = models.PositiveIntegerField()
    fecha_inicio = models.DateField()
    fecha_final = models.DateField()
    
    def __str__(self):
        return f"Semana {self.numero_semana} ({self.fecha_inicio} - {self.fecha_final})"