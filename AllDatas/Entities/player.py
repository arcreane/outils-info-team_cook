from pathlib import Path

import pygame
import os
import sys
import settings

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))# Import simple car le chemin est géré par main.py


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
        self.taille = 80
        super().__init__(settings.LARGEUR_ECRAN // 2 - self.taille // 2, 500, self.taille, self.taille, (0, 255, 0), 3)

        chemin_actuel = os.path.dirname(__file__)
        chemin_image = os.path.join(chemin_actuel, "..", "Assets", "vaisseau.png")

        try:
            img_originale = pygame.image.load(chemin_image).convert_alpha()
            self.image = pygame.transform.scale(img_originale, (self.taille, self.taille))
        except Exception:
            pass

        self.vitesse = 5
        self.invincible = False
        self.temps_invincibilite = 0
        self.last_shot_time = 0
        self.fire_delay = 200

    def update(self):
        keys = pygame.key.get_pressed()

        if (keys[pygame.K_LEFT] or keys[pygame.K_q]) and self.rect.left > 0:
            self.rect.x -= self.vitesse
        if (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and self.rect.right < settings.LARGEUR_ECRAN:
            self.rect.x += self.vitesse

        if self.invincible:
            self.temps_invincibilite -= 1
            if self.temps_invincibilite <= 0:
                self.invincible = False

    def shoot(self, current_time):
        if current_time - self.last_shot_time > self.fire_delay:
            self.last_shot_time = current_time
            return Shoot(self.rect.centerx, self.rect.top)
        return None

    def degat(self, valeur):
        if not self.invincible:
            self.vie -= valeur
            self.invincible = True
            self.temps_invincibilite = 60