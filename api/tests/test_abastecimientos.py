import unittest
from django.test import TestCase
from datetime import date
from api.manicuristas.models import Manicurista
from api.abastecimientos.models import Abastecimiento


class AbastecimientoDjangoTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.manicurista = Manicurista.objects.create(nombre="Ana")
        cls.abastecimiento = Abastecimiento.objects.create(
            fecha=date.today(),
            cantidad=15,
            manicurista=cls.manicurista
        )

    def test_cantidad(self):
        self.assertEqual(self.abastecimiento.cantidad, 15)

    def test_fecha(self):
        self.assertEqual(self.abastecimiento.fecha, date.today())

    def test_relacion_manicurista(self):
        self.assertEqual(self.abastecimiento.manicurista.nombre, "Ana")

    def test_str(self):
        esperado = f"Abastecimiento {self.abastecimiento.id} - {self.abastecimiento.manicurista} ({self.abastecimiento.fecha})"
        self.assertEqual(str(self.abastecimiento), esperado)

    def test_tipo_abastecimiento(self):
        self.assertTrue(isinstance(self.abastecimiento, Abastecimiento))
