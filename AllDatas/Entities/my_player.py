import pygame
from entities import Entity


class Player(Entity):
    def __init__(self):
        #joueur centré + 3 vies
        super().__init__(375, 500, 50, 50, (0, 255, 0), 3)
        self.vitesse = 5
        #nvincibilité tempo après dégât
        self.invincible = False
        self.temps_invincibilite = 0

    def update(self):
        #Deplacement avec fleches directionelles
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.vitesse
        if keys[pygame.K_RIGHT] and self.rect.right < 800:
            self.rect.x += self.vitesse

        #système d'invincibilité
        if self.invincible:
            self.temps_invincibilite -= 1
            if self.temps_invincibilite <= 0:
                self.invincible = False

    def degat(self, valeur):
        if not self.invincible:
            self.vie -= valeur
            self.invincible = True
            self.temps_invincibilite = 120
            print(f"A ! {self.vie} vies")  # Debug pour voir les vies restantes