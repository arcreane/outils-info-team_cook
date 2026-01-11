import pygame
import random
from .entities import Entity
from settings import HAUTEUR_ECRAN, LARGEUR_ECRAN # Importation pour éviter les valeurs en dur

class Ennemi(Entity):
    def __init__(self, x, y):
        vitesse_aleatoire = random.randint(2, 5)
        super().__init__(x, y, 40, 40, (255, 0, 0), 1)
        self.vitesse = vitesse_aleatoire

    def update(self):
        self.rect.y += self.vitesse
        # Si l'ennemi sort de l'écran par le bas
        if self.rect.top > HAUTEUR_ECRAN:
            self.respawn()
            return True # Signal qu'un ennemi s'est échappé
        return False

    def respawn(self):
        self.rect.y = random.randint(-150, -50)
        self.rect.x = random.randint(0, LARGEUR_ECRAN - 40)
        self.vitesse = random.randint(2, 5)