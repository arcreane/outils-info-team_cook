import pygame
import random


class Ennemi(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((40, 40))
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.vitesse = random.randint(1, 3)
        self.vie = 1  # Un ennemi meurt en 1 coup

    def update(self):
        self.rect.y += self.vitesse
        if self.rect.y > 600:
            self.rect.y = -40
            self.rect.x = random.randint(0, 760)