from django.urls import path, include
from rest_framework.routers import DefaultRouter
from api.views.usuariosViews import UsuarioViewSet
from api.views.clientesViews import ClienteViewSet
from api.views.manicuristasViews import ManicuristaViewSet

router = DefaultRouter()
router.register(r'usuarios', UsuarioViewSet, basename='usuario')
router.register(r'clientes', ClienteViewSet, basename='cliente')
router.register(r'manicuristas', ManicuristaViewSet, basename='manicurista')

urlpatterns = [
    path('', include(router.urls)),
]

usuarios_urlpatterns = urlpatterns
