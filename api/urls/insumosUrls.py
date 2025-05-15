from django.urls import path, include
from rest_framework.routers import DefaultRouter
from api.views.proveedoresViews import ProveedorViewSet
from api.views.comprasViews import CompraViewSet
from api.views.categoriainsumosViews import CategoriaInsumoViewSet
from api.views.insumosViews import InsumoViewSet
from api.views.comprahasinsumosViews import CompraHasInsumoViewSet

router = DefaultRouter()
router.register(r'proveedores', ProveedorViewSet, basename='proveedor')
router.register(r'compras', CompraViewSet, basename='compra')
router.register(r'categorias-insumos', CategoriaInsumoViewSet, basename='categoria-insumo')
router.register(r'insumos', InsumoViewSet, basename='insumo')
router.register(r'compras-insumos', CompraHasInsumoViewSet, basename='compra-insumo')

urlpatterns = [
    path('', include(router.urls)),
]

insumos_urlpatterns = urlpatterns