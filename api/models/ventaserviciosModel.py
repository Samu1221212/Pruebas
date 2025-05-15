from django.db import models
from django.core.validators import MinValueValidator
from .base import BaseModel
from .clientesModel import Cliente
from .manicuristasModel import Manicurista
from .serviciosModel import Servicio


class VentaServicio(BaseModel):
    fecha = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    cliente = models.ForeignKey(Cliente, on_delete=models.PROTECT)
    manicurista = models.ForeignKey(Manicurista, on_delete=models.PROTECT)
    servicio = models.ForeignKey(Servicio, on_delete=models.PROTECT)
    
    def __str__(self):
        return f"Venta {self.id} - {self.cliente.nombre} ({self.fecha.strftime('%Y-%m-%d')})"