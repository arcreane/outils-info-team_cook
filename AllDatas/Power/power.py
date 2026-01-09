import pygame
from entities import Entity

class Power(Entity):
    """
    Power-up ramassable par le joueur
    type :
      - "rapid_fire" : tire plus vite
      - "big_fire"   : boules de feu plus grosses
    """

    def __init__(self, x, y, power_type="rapid_fire"):
        super().__init__(x, y, 30, 30, (255, 165, 0), 1)
        self.power_type = power_type
        self.vitesse = 2

    def update(self):
        # Le power descend vers le bas
        self.rect.y += self.vitesse

        # Supprimer si hors écran
        if self.rect.top > 600:
            self.kill()

    def apply(self, player):
        """Applique l'effet au joueur"""
        if self.power_type == "rapid_fire":
            player.fire_delay = max(80, player.fire_delay - 100)

        elif self.power_type == "big_fire":
            player.big_fire = True

        self.kill()
