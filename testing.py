import sys
import os
import unittest
import pygame

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from AllDatas.Entities.player import Player
from AllDatas.Entities.ennemi import Ennemi
from settings import HAUTEUR_ECRAN


class TestFireballGame(unittest.TestCase):
    def setUp(self):
        self.player = Player()

    def test_controles_clavier_60(self):
        """Vérifie que le joueur peut bouger avec Q et D"""
        pos_initiale = self.player.rect.x
        self.player.rect.x += self.player.vitesse
        self.assertGreater(self.player.rect.x, pos_initiale)
        self.player.rect.x -= self.player.vitesse
        self.assertEqual(self.player.rect.x, pos_initiale)

    def test_perte_vie_et_invincibilite(self):
        """Vérifie que le joueur perd une vie si il est touché par un mob, et est ensuite invinsible"""
        vie_depart = self.player.vie
        self.player.degat(1)

        self.assertEqual(self.player.vie, vie_depart - 1)
        self.assertTrue(self.player.invincible)

    def test_ennemi_sortie_ecran(self):
        """Vérifie qu'un ennemi qui sort fait perdre une vie au player"""
        ennemi = Ennemi(100, HAUTEUR_ECRAN + 10)
        # La méthode update doit renvoyer True si l'ennemi dépasse le bas
        sorti = ennemi.update()
        self.assertTrue(sorti)


if __name__ == '__main__':
    unittest.main()