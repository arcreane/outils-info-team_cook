import pygame
import os
from .entities import Entity
from settings import LARGEUR_ECRAN  # Importation pour les limites de l'écran


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
        # Initialisation de base
        super().__init__(375, 500, 50, 50, (0, 255, 0), 3)

        # --- Chargement du Sprite ---
        # On remonte d'un dossier (..) pour aller dans Assets
        chemin_actuel = os.path.dirname(__file__)
        chemin_image = os.path.join(chemin_actuel, "..", "Assets", "vaisseau.png")

        try:
            # .convert_alpha() préserve la transparence du PNG
            img_originale = pygame.image.load(chemin_image).convert_alpha()
            # On redimensionne l'image pour qu'elle corresponde aux 50x50 de l'Entity
            self.image = pygame.transform.scale(img_originale, (50, 50))
        except Exception as e:
            print(f"Erreur lors du chargement de l'image : {e}")

        self.vitesse = 5
        self.invincible = False
        self.temps_invincibilite = 0

        # Variables nécessaires pour le tir (utilisées par game.py)
        self.last_shot_time = 0
        self.fire_delay = 200

    def update(self):
        keys = pygame.key.get_pressed()

        # Déplacements avec limites d'écran
        if (keys[pygame.K_LEFT] or keys[pygame.K_q]) and self.rect.left > 0:
            self.rect.x -= self.vitesse
        if (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and self.rect.right < LARGEUR_ECRAN:
            self.rect.x += self.vitesse

        # Gestion de l'invincibilité
        if self.invincible:
            self.temps_invincibilite -= 1
            if self.temps_invincibilite <= 0:
                self.invincible = False

    def shoot(self, current_time):
        """Méthode nécessaire pour le fonctionnement de game.py"""
        if current_time - self.last_shot_time > self.fire_delay:
            self.last_shot_time = current_time
            return Shoot(self.rect.centerx, self.rect.top)
        return None

    def degat(self, valeur):
        if not self.invincible:
            self.vie -= valeur
            self.invincible = True
            self.temps_invincibilite = 60
