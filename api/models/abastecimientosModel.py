from django.db import models
from .base import BaseModel
from .manicuristasModel import Manicurista

class Abastecimiento(BaseModel):
    fecha = models.DateField()
    cantidad = models.PositiveIntegerField()
    manicurista = models.ForeignKey(Manicurista, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"Abastecimiento {self.id} - {self.manicurista} ({self.fecha})"