import pygame
import random


class Ennemi:
    def __init__(self, x, y, vitesse):
        # Statistiques de base
        self.hp = 50
        self.vitesse = vitesse

        self.image = pygame.Surface((40, 40))
        self.image.fill((255, 0, 0))  # ennemi rouge
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def deplacer(self):
        """Fait descendre l'ennemi"""
        self.rect.y += self.vitesse

    def degats(self, montant):
        """Réduit les PV de l'ennemi"""
        self.hp -= montant
        if self.hp <= 0:
            print("L'ennemi est mort !")

    def dessiner(self, ecran):
        """Affiche l'ennemi sur la fenêtre du jeu"""
        ecran.blit(self.image, self.rect)