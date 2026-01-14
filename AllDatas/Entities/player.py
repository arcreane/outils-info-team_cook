import pygame
from .entities import Entity

class Shoot(Entity):
    def __init__(self, x, y):
        super().__init__(x, y, 10, 20, (255, 255, 0), 1)
        self.vitesse = 10
        self.rect.centerx = x

    def update(self):
        self.rect.y -= self.vitesse
        if self.rect.bottom < 0:
            self.kill()

class Player(Entity):
    def __init__(self):
        super().__init__(375, 500, 50, 50, (0, 255, 0), 3)
        self.vitesse = 5
        self.invincible = False
        self.temps_invincibilite = 0

    def update(self):
        keys = pygame.key.get_pressed()
        if (keys[pygame.K_LEFT] or keys[pygame.K_q]) and self.rect.left > 0:
            self.rect.x -= self.vitesse
        if (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and self.rect.right < 800:
            self.rect.x += self.vitesse

        if self.invincible:
            self.temps_invincibilite -= 1
            if self.temps_invincibilite <= 0:
                self.invincible = False

    def degat(self, valeur):
        if not self.invincible:
            self.vie -= valeur
            self.invincible = True
            self.temps_invincibilite = 60