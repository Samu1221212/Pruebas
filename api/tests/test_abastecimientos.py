import unittest
from django.test import TestCase
from datetime import date
from api.manicuristas.models import Manicurista
from api.abastecimientos.models import Abastecimiento


class AbastecimientoUnitTest(unittest.TestCase):

    def test_operacion_basica(self):
        self.assertEqual(2 + 2, 4)


class AbastecimientoDjangoTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        # Crear Manicurista con campos obligatorios mínimos
        cls.manicurista = Manicurista.objects.create(nombre="Ana")

        # Crear Abastecimiento asociado
        cls.abastecimiento = Abastecimiento.objects.create(
            fecha=date.today(),
            cantidad=15,
            manicurista=cls.manicurista
        )

    def test_cantidad(self):
        self.assertEqual(self.abastecimiento.cantidad, 15)

    def test_str(self):
        esperado = f"Abastecimiento {self.abastecimiento.id} - {self.abastecimiento.manicurista} ({self.abastecimiento.fecha})"
        self.assertEqual(str(self.abastecimiento), esperado)
