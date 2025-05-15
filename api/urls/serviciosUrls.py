from django.urls import path, include
from rest_framework.routers import DefaultRouter
from api.views.serviciosViews import ServicioViewSet
from api.views.agendamientocitasViews import AgendamientoCitaViewSet
from api.views.ventaserviciosViews import VentaServicioViewSet

router = DefaultRouter()
router.register(r'servicios', ServicioViewSet, basename='servicio')
router.register(r'citas', AgendamientoCitaViewSet, basename='cita')
router.register(r'ventas-servicios', VentaServicioViewSet, basename='venta-servicio')

urlpatterns = [
    path('', include(router.urls)),
]

servicios_urlpatterns = urlpatterns