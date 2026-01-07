import pygame

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill((0, 255, 0))
        self.rect = self.image.get_rect()
        self.rect.center = (400, 500)
        self.vitesse = 5
        self.vie = 3  # Système de vie du joueur

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.vitesse
        if keys[pygame.K_RIGHT] and self.rect.right < 800:
            self.rect.x += self.vitesse