import pygame
from entities import Entity

class Shoot(Entity):
    def __init__(self, x, y):
        #tir jaune de 10x20 pixels
        super().__init__(x, y, 10, 20, (255, 255, 0), 1)
        self.vitesse = 10
        #tir centré
        self.rect.centerx = x

    def update(self):
        self.rect.y -= self.vitesse
        if self.rect.bottom < 0:
            self.kill()

