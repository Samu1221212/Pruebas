from django.urls import path, include
from rest_framework.routers import DefaultRouter
from api.views.novedadesViews import NovedadViewSet
from api.views.semanasViews import SemanaViewSet
from api.views.liquidacionesViews import LiquidacionViewSet
from api.views.abastecimientosViews import AbastecimientoViewSet
from api.views.insumohasabastecimientosViews import InsumoHasAbastecimientoViewSet

router = DefaultRouter()
router.register(r'novedades', NovedadViewSet, basename='novedad')
router.register(r'semanas', SemanaViewSet, basename='semana')
router.register(r'liquidaciones', LiquidacionViewSet, basename='liquidacion')
router.register(r'abastecimientos', AbastecimientoViewSet, basename='abastecimiento')
router.register(r'abastecimientos-insumos', InsumoHasAbastecimientoViewSet, basename='abastecimiento-insumo')

urlpatterns = [
    path('', include(router.urls)),
]

operaciones_urlpatterns = urlpatterns