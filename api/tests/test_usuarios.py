import unittest
from django.test import TestCase
from api.roles.models import Rol
from api.usuarios.models import Usuario


class UsuarioUnitTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Se ejecuta una vez antes de todas las pruebas
        super().setUpClass()
        cls.rol = Rol.objects.create(nombre="Usuario Normal")

    def test_crear_usuario(self):
        usuario = Usuario.objects.create_user(
            correo_electronico="usuario@unit.com",
            password="unitpass123",
            nombre="User Unit",
            tipo_documento="CC",
            documento="111222333",
            celular="+3001234567",
            rol=self.rol,
        )
        self.assertEqual(usuario.correo_electronico, "usuario@unit.com")
        self.assertEqual(str(usuario), "User Unit (usuario@unit.com)")


class UsuarioDjangoTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        # Se ejecuta una sola vez para todos los tests en esta clase
        cls.rol = Rol.objects.create(nombre="Usuario Normal")

    def test_crear_usuario(self):
        usuario = Usuario.objects.create_user(
            correo_electronico="usuario@testcase.com",
            password="testcasepass",
            nombre="User TestCase",
            tipo_documento="CC",
            documento="444555666",
            celular="+3109876543",
            rol=self.rol,
        )
        self.assertEqual(usuario.correo_electronico, "usuario@testcase.com")
        self.assertEqual(str(usuario), "User TestCase (usuario@testcase.com)")