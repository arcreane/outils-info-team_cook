import pygame

class Shoot(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((10, 20))
        self.image.fill((255, 255, 0)) # Jaune
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.vitesse = 10

    def update(self):
        # Le tir monte
        self.rect.y -= self.vitesse
        # Si le tir sort de l'écran, on le supprime du jeu
        if self.rect.bottom < 0:
            self.kill()