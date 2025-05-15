from django.db import models
from .base import BaseModel
from .clientesModel import Cliente
from .manicuristasModel import Manicurista
from .ventaserviciosModel import VentaServicio


class AgendamientoCita(BaseModel):
    ESTADO_CHOICES = (
        ('pendiente', 'Pendiente'),
        ('en_proceso', 'En Proceso'),
        ('finalizado', 'Finalizado'),
        ('cancelado', 'Cancelado'),
    )
    
    hora_entrada = models.DateTimeField()
    hora_salida = models.DateTimeField()
    estado = models.CharField(max_length=15, choices=ESTADO_CHOICES, default='pendiente')
    cliente = models.ForeignKey(Cliente, on_delete=models.PROTECT)
    manicurista = models.ForeignKey(Manicurista, on_delete=models.PROTECT)
    venta_servicio = models.OneToOneField(VentaServicio, on_delete=models.SET_NULL, null=True, blank=True)
    
    def __str__(self):
        return f"Cita {self.id} - {self.cliente.nombre} con {self.manicurista} ({self.hora_entrada.strftime('%Y-%m-%d %H:%M')})"
    
    class Meta:
        verbose_name = "Agendamiento de Cita"
        verbose_name_plural = "Agendamientos de Citas"