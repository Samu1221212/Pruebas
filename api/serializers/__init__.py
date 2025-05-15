# serializers/__init__.py

# Importamos todos los serializers para facilitar su acceso
from .usuariosSerializer import UsuarioSerializer
from .clientesSerializer import ClienteSerializer
from .rolesSerializer import RolSerializer, PermisoSerializer, RolHasPermisoSerializer
from .manicuristasSerializer import ManicuristaSerializer
from .proveedoresSerializer import ProveedorSerializer
from .comprasSerializer import CompraSerializer
from .categoriainsumoSerializer import CategoriaInsumoSerializer
from .insumosSerializer import InsumoSerializer
from .comprahasinsumoSerializer import CompraHasInsumoSerializer
from .novedadesSerializer import NovedadSerializer
from .semanasSerializer import SemanaSerializer
from .liquidacionesSerializer import LiquidacionSerializer
from .abastecimientosSerializer import AbastecimientoSerializer
from .insumohasabastecimientoSerializer import InsumoHasAbastecimientoSerializer
from .serviciosSerializer import ServicioSerializer
from .agendamientocitasSerializer import AgendamientoCitaSerializer
from .ventaserviciosSerializer import VentaServicioSerializer

# Esto permite importar todos los serializers directamente desde el paquete serializers
__all__ = [
    'UsuarioSerializer',
    'ClienteSerializer',
    'RolSerializer',
    'PermisoSerializer',
    'RolHasPermisoSerializer',
    'ManicuristaSerializer',
    'ProveedorSerializer',
    'CompraSerializer',
    'CategoriaInsumoSerializer',
    'InsumoSerializer',
    'CompraHasInsumoSerializer',
    'NovedadSerializer',
    'SemanaSerializer',
    'LiquidacionSerializer',
    'AbastecimientoSerializer',
    'InsumoHasAbastecimientoSerializer',
    'ServicioSerializer',
    'AgendamientoCitaSerializer',
    'VentaServicioSerializer',
]