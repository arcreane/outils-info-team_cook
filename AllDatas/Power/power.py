import pygame
from entities import Entity

class Power(Entity):
    """
    Power-up ramassable par le joueur.
    Version corrigée : utilise self.kill() pour une gestion propre de la mémoire.
    """

    def __init__(self, x, y, power_type="rapid_fire"):
        # Initialisation via la classe parente (position, taille, couleur, layer)
        super().__init__(x, y, 30, 30, (255, 165, 0), 1)
        self.power_type = power_type
        self.vitesse = 2

    def update(self):
        """Met à jour la position et nettoie si nécessaire."""
        # Le bonus descend
        self.rect.y += self.vitesse


        if self.rect.top > 600:

            self.kill()

    def apply(self, player):
        """Applique l'effet au joueur et disparaît."""
        if self.power_type == "rapid_fire":
            player.fire_delay = max(80, player.fire_delay - 100)
        elif self.power_type == "big_fire":
            player.big_fire = True


        self.kill()