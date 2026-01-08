import pygame
import random
from entities import Entity

class Ennemi(Entity):
    def __init__(self, x, y):
        vitesse_aleatoire = random.randint(1, 3)
        super().__init__(x, y, 40, 40, (255, 0, 0), 1)
        self.vitesse = vitesse_aleatoire

    def update(self):
        self.rect.y += self.vitesse
        if self.rect.y > 600:
            self.rect.y = -40
            self.rect.x = random.randint(0, 760)