# models/__init__.py

# models/__init__.py

# Importamos todos los modelos para facilitar su acceso
from .usuariosModel import Usuario
from .clientesModel import Cliente
from .rolesModel import Rol, Permiso, RolHasPermiso
from .manicuristasModel import Manicurista
from .proveedoresModel import Proveedor
from .comprasModel import Compra
from .categoriainsumoModel import CategoriaInsumo
from .insumosModel import Insumo
from .comprahasinsumoModel import CompraHasInsumo
from .novedadesModel import Novedad
from .semanasModel import Semana
from .liquidacionesModel import Liquidacion
from .abastecimientosModel import Abastecimiento
from .insumohasabastecimientoModel import InsumoHasAbastecimiento
from .serviciosModel import Servicio
from .agendamientocitasModel import AgendamientoCita
from .ventaserviciosModel import VentaServicio

# Esto permite importar todos los modelos directamente desde el paquete models
__all__ = [
    'Usuario',
    'Cliente',
    'Rol',
    'Permiso',
    'RolHasPermiso',
    'Manicurista',
    'Proveedor',
    'Compra',
    'CategoriaInsumo',
    'Insumo',
    'CompraHasInsumo',
    'Novedad',
    'Semana',
    'Liquidacion',
    'Abastecimiento',
    'InsumoHasAbastecimiento',
    'Servicio',
    'AgendamientoCita',
    'VentaServicio',
]