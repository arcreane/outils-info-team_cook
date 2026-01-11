import pygame
from entities import Entity
from shoot import Shoot

class Player(Entity):
    def __init__(self):
        super().__init__(375, 500, 50, 50, (0, 255, 0), 3)
        self.vitesse = 5
        self.invincible = False
        self.temps_invincibilite = 0
        self.last_shot_time = 0
        self.fire_delay = 200

    def update(self):
        keys = pygame.key.get_pressed()
        if (keys[pygame.K_LEFT] or keys[pygame.K_q]) and self.rect.left > 0:
            self.rect.x -= self.vitesse
        if (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and self.rect.right < 800:
            self.rect.x += self.vitesse
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.vitesse
        if keys[pygame.K_RIGHT] and self.rect.right < 800:
            self.rect.x += self.vitesse

        if self.invincible:
            self.temps_invincibilite -= 1
            if self.temps_invincibilite <= 0:
                self.invincible = False

    def shoot(self, current_time):
        """Gère la logique de tir en interne"""
        if current_time - self.last_shot_time > self.fire_delay:
            self.last_shot_time = current_time
            return Shoot(self.rect.centerx, self.rect.top)
        return None

    def degat(self, valeur):
        if not self.invincible:
            self.vie -= valeur
            self.invincible = True
            self.temps_invincibilite = 60 # Réduit un peu pour la fluidité (1 sec à 60fps)