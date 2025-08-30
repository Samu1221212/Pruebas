from django.test import TestCase
from django.core.exceptions import ValidationError
from api.categoriainsumos.models import CategoriaInsumo
from api.insumos.models import Insumo

class InsumoModelTestCase(TestCase):
    """Pruebas del modelo Insumo."""

    @classmethod
    def setUpTestData(cls):
        """Crear datos de prueba para todas las pruebas."""
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

    def test_nombre_asignado_correctamente(self):
        """Verifica que el nombre se haya guardado correctamente."""
        self.assertEqual(self.insumo.nombre, "Insumo Test")

    def test_cantidad_asignada_correctamente(self):
        """Verifica que la cantidad se haya guardado correctamente."""
        self.assertEqual(self.insumo.cantidad, 10)

    def test_estado_asignado_correctamente(self):
        """Verifica que el estado se haya guardado correctamente."""
        self.assertEqual(self.insumo.estado, "activo")

    def test_str_retorna_nombre(self):
        """Verifica que el método __str__ devuelva el nombre del insumo."""
        self.assertEqual(str(self.insumo), self.insumo.nombre)

    def test_nombre_obligatorio(self):
        """No debe permitir crear un insumo sin nombre."""
        insumo = Insumo(cantidad=5, estado="activo", categoria_insumo=self.categoria)
        with self.assertRaises(ValidationError):
            insumo.full_clean()

    def test_cantidad_no_negativa(self):
        """No debe permitir crear un insumo con cantidad negativa."""
        insumo = Insumo(nombre="Test", cantidad=-5, estado="activo", categoria_insumo=self.categoria)
        with self.assertRaises(ValidationError):
            insumo.full_clean()

    def test_estado_valido(self):
        """No debe permitir crear un insumo con estado inválido."""
        insumo = Insumo(nombre="Test", cantidad=5, estado="invalido", categoria_insumo=self.categoria)
        with self.assertRaises(ValidationError):
            insumo.full_clean()

    def test_categoria_obligatoria(self):
        """No debe permitir crear un insumo sin categoría asignada."""
        insumo = Insumo(nombre="Test", cantidad=5, estado="activo", categoria_insumo=None)
        with self.assertRaises(ValidationError):
            insumo.full_clean()
