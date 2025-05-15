# api/urls/__init__.py

from django.urls import path, include
from .authUrls import auth_urlpatterns
from .recuperacionUrls import recuperacion_urlpatterns
from .usuariosUrls import usuarios_urlpatterns
from .rolesUrls import roles_urlpatterns
from .insumosUrls import insumos_urlpatterns
from .operacionesUrls import operaciones_urlpatterns
from .serviciosUrls import servicios_urlpatterns

# Agrupamos todos los patrones de URL
urlpatterns = [
    path('auth/', include(auth_urlpatterns)),
    path('recuperacion/', include(recuperacion_urlpatterns)),
    path('usuarios/', include(usuarios_urlpatterns)),
    path('roles/', include(roles_urlpatterns)),
    path('insumos/', include(insumos_urlpatterns)),
    path('operaciones/', include(operaciones_urlpatterns)),
    path('servicios/', include(servicios_urlpatterns)),
]
