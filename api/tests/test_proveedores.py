from django.test import TestCase
from api.proveedores.models import Proveedor

class ProveedorTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        # Crear un proveedor para las pruebas
        cls.proveedor = Proveedor.objects.create(
            tipo_persona='natural',
            nombre_empresa='Empresa Test',
            nit='123456789',
            nombre='Pedro Perez',
            direccion='Calle Falsa 123',
            correo_electronico='contacto@empresa.com',
            celular='+12345678901',
            estado='activo'
        )

    def test_nombre_empresa(self):
        self.assertEqual(self.proveedor.nombre_empresa, 'Empresa Test')

    def test_estado_default(self):
        self.assertEqual(self.proveedor.estado, 'activo')

    def test_str(self):
        esperado = f"{self.proveedor.nombre_empresa} ({self.proveedor.nit})"
        self.assertEqual(str(self.proveedor), esperado)