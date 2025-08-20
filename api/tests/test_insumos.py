import unittest
from django.test import TestCase
from api.categoriainsumos.models import CategoriaInsumo
from api.insumos.models import Insumo

class InsumoUnitTest(unittest.TestCase):

    def test_operacion_basica(self):
        self.assertEqual(3 * 3, 9)


class InsumoDjangoTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.categoria = CategoriaInsumo.objects.create(
            nombre="Categoría Test",
            estado="activo"
        )
        cls.insumo = Insumo.objects.create(
            nombre="Insumo Test",
            cantidad=10,
            estado="activo",
            categoria_insumo=cls.categoria
        )

    def test_nombre(self):
        self.assertEqual(self.insumo.nombre, "Insumo Test")

    def test_cantidad(self):
        self.assertEqual(self.insumo.cantidad, 10)

    def test_estado(self):
        self.assertEqual(self.insumo.estado, "activo")

    def test_str(self):
        self.assertEqual(str(self.insumo), "Insumo Test")
