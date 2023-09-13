from django.test import TestCase
from login.models import DatosUsuario

# Create your tests here.


class Tests(TestCase):
    # Esto retorna False cuando debería retornar true
    def test_1(self):
        result = DatosUsuario.objects.filter(country="Argentina").exists()
        self.assertTrue(result)

    # Si hago esto funciona
    """def setUp(self):
        DatosUsuario.objects.create(country="Argentina")
    
    def test_1(self):
        result = DatosUsuario.objects.filter(country="Argentina").exists()
        self.assertTrue(result)"""
