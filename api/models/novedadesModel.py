from django.db import models
from .base import BaseModel
from .manicuristasModel import Manicurista


class Novedad(BaseModel):
    ESTADO_CHOICES = (
        ('presente', 'Presente'),
        ('ausente', 'Ausente'),
        ('tardanza', 'Tardanza'),
    )
    
    hora_entrada = models.TimeField()
    hora_salida = models.TimeField(null=True, blank=True)
    estado = models.CharField(max_length=10, choices=ESTADO_CHOICES)
    motivo = models.TextField(blank=True, null=True)
    manicurista = models.ForeignKey(Manicurista, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.manicurista} - {self.estado} ({self.hora_entrada.strftime('%Y-%m-%d')})"
    
    class Meta:
        verbose_name_plural = "Novedades"