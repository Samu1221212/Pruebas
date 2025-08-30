from django.test import TestCase
from django.core.exceptions import ValidationError
from api.categoriainsumos.models import CategoriaInsumo

class CategoriaInsumoModelTestCase(TestCase):
    """Pruebas del modelo CategoriaInsumo."""

    @classmethod
    def setUpTestData(cls):
        """Crear una categoría de prueba válida para todos los tests."""
        cls.categoria = CategoriaInsumo.objects.create(
            nombre="Categoría de Prueba",
            estado="activo"
        )

    def test_nombre_asignado_correctamente(self):
        """Verifica que el nombre se haya guardado correctamente."""
        self.assertEqual(self.categoria.nombre, "Categoría de Prueba")

    def test_estado_asignado_correctamente(self):
        """Verifica que el estado se haya guardado correctamente."""
        self.assertEqual(self.categoria.estado, "activo")

    def test_str_retorna_nombre(self):
        """Verifica que el método __str__ devuelva el nombre de la categoría."""
        self.assertEqual(str(self.categoria), self.categoria.nombre)

    def test_nombre_obligatorio(self):
        """No debe permitir crear una categoría sin nombre."""
        categoria = CategoriaInsumo(estado="activo")
        with self.assertRaises(ValidationError):
            categoria.full_clean()  # Valida los campos según el modelo

    def test_estado_valido(self):
        """No debe permitir crear una categoría con estado inválido."""
        categoria = CategoriaInsumo(nombre="Test", estado="invalido")
        with self.assertRaises(ValidationError):
            categoria.full_clean()  # Valida los campos según el modelo
