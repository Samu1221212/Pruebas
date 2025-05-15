# views/__init__.py

# Importamos todos los viewsets para facilitar su acceso
from .usuariosViews import UsuarioViewSet
from .clientesViews import ClienteViewSet
from .rolesViews import RolViewSet, PermisoViewSet, RolHasPermisoViewSet
from .manicuristasViews import ManicuristaViewSet
from .proveedoresViews import ProveedorViewSet
from .comprasViews import CompraViewSet
from .categoriainsumosViews import CategoriaInsumoViewSet
from .insumosViews import InsumoViewSet
from .comprahasinsumosViews import CompraHasInsumoViewSet
from .novedadesViews import NovedadViewSet
from .semanasViews import SemanaViewSet
from .liquidacionesViews import LiquidacionViewSet
from .abastecimientosViews import AbastecimientoViewSet
from .insumohasabastecimientosViews import InsumoHasAbastecimientoViewSet
from .serviciosViews import ServicioViewSet
from .agendamientocitasViews import AgendamientoCitaViewSet
from .ventaserviciosViews import VentaServicioViewSet

# Esto permite importar todos los viewsets directamente desde el paquete views
__all__ = [
    'UsuarioViewSet',
    'ClienteViewSet',
    'RolViewSet',
    'PermisoViewSet',
    'RolHasPermisoViewSet',
    'ManicuristaViewSet',
    'ProveedorViewSet',
    'CompraViewSet',
    'CategoriaInsumoViewSet',
    'InsumoViewSet',
    'CompraHasInsumoViewSet',
    'NovedadViewSet',
    'SemanaViewSet',
    'LiquidacionViewSet',
    'AbastecimientoViewSet',
    'InsumoHasAbastecimientoViewSet',
    'ServicioViewSet',
    'AgendamientoCitaViewSet',
    'VentaServicioViewSet',
]