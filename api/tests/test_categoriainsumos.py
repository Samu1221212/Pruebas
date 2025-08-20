import unittest
from django.test import TestCase
from api.categoriainsumos.models import CategoriaInsumo

class CategoriaInsumoUnitTest(unittest.TestCase):

    def test_operacion_basica(self):
        self.assertEqual(1 + 1, 2)

class CategoriaInsumoDjangoTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.categoria = CategoriaInsumo.objects.create(
            nombre="Categoría de Prueba",
            estado="activo"
        )

    def test_nombre(self):
        self.assertEqual(self.categoria.nombre, "Categoría de Prueba")

    def test_estado_default(self):
        self.assertEqual(self.categoria.estado, "activo")

    def test_str(self):
        self.assertEqual(str(self.categoria), "Categoría de Prueba")