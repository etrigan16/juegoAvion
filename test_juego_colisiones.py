import unittest
from unittest.mock import patch, Mock
import pygame
from main import generar_obstaculo, generar_nube, reiniciar_juego, mostrar_cuenta_regresiva, mostrar_game_over

pygame.init()

class TestJuegoAvion(unittest.TestCase):

    def setUp(self):
        # Inicializar variables globales antes de cada prueba
        global avion_x, avion_y, obstaculos, nubes, mostrar_explosion, inmovilizado, vidas
        avion_x = 100
        avion_y = 768 // 2
        obstaculos = []
        nubes = []
        mostrar_explosion = False
        inmovilizado = False
        vidas = 3

    @patch('pygame.image.load')
    @patch('pygame.transform.scale')
    def generar_obstaculo_crea_obstaculo_correctamente(self, mock_scale, mock_load):
        # Simular la carga y escalado de imágenes
        mock_load.return_value = Mock()
        mock_scale.return_value = Mock()
        # Generar un obstáculo y verificar su estructura
        obstaculo = generar_obstaculo()
        self.assertEqual(len(obstaculo), 4)
        self.assertIsInstance(obstaculo[0], int)
        self.assertIsInstance(obstaculo[1], int)
        self.assertIsInstance(obstaculo[2], pygame.Surface)
        self.assertIsInstance(obstaculo[3], pygame.Rect)

    @patch('pygame.image.load')
    @patch('pygame.transform.scale')
    def generar_nube_crea_nube_correctamente(self, mock_scale, mock_load):
        # Simular la carga y escalado de imágenes
        mock_load.return_value = Mock()
        mock_scale.return_value = Mock()
        # Generar una nube y verificar su estructura
        nube = generar_nube()
        self.assertEqual(len(nube), 4)
        self.assertIsInstance(nube[0], int)
        self.assertIsInstance(nube[1], int)
        self.assertIsInstance(nube[2], pygame.Surface)
        self.assertIsInstance(nube[3], pygame.Rect)

    @patch('pygame.time.wait')
    def reiniciar_juego_reinicia_correctamente(self, mock_wait):
        # Reiniciar el juego y verificar el estado de las variables globales
        global avion_x, avion_y, obstaculos, nubes, mostrar_explosion, inmovilizado, vidas
        reiniciar_juego()
        self.assertEqual(avion_x, 100)
        self.assertEqual(avion_y, 768 // 2)
        self.assertEqual(obstaculos, [])
        self.assertEqual(nubes, [])
        self.assertFalse(mostrar_explosion)
        self.assertFalse(inmovilizado)
        self.assertEqual(vidas, 2)

    @patch('pygame.display.flip')
    @patch('pygame.time.wait')
    def mostrar_cuenta_regresiva_muestra_correctamente(self, mock_wait, mock_flip):
        # Verificar que la cuenta regresiva se muestra correctamente
        mostrar_cuenta_regresiva()
        self.assertEqual(mock_wait.call_count, 4)
        self.assertEqual(mock_flip.call_count, 4)

    @patch('pygame.display.flip')
    @patch('pygame.time.wait')
    def mostrar_game_over_muestra_correctamente(self, mock_wait, mock_flip):
        # Verificar que la pantalla de "Game Over" se muestra correctamente
        mostrar_game_over()
        self.assertEqual(mock_wait.call_count, 1)
        self.assertEqual(mock_flip.call_count, 1)

if __name__ == '__main__':
    unittest.main()