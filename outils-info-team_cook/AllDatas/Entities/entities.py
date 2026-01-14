import pygame

class Entity(pygame.sprite.Sprite):
    def __init__(self, x, y, largeur, hauteur, couleur, vie):
        super().__init__()
        self.image = pygame.Surface((largeur, hauteur))
        self.image.fill(couleur)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.vie = vie
        self.vie_max = vie

    def degat(self, valeur):
        #-1 vie si dégat
        self.vie -= valeur
        #si plus de vie -- mort
        if self.vie <= 0:
            self.kill()