import pygame
from Player_Info.player import Player  # Si tu as déplacé le fichier
from ennemi import Ennemi

# Initialisation
pygame.init()
ecran = pygame.display.set_mode((800, 600))
joueur = Player()
ennemis = [Ennemi(), Ennemi()]

#Game Loop
continuer = True
while continuer:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            continuer = False

    joueur.update()
    ecran.fill((0, 0, 0))  # Fond noir
    joueur.dessiner(ecran)
    pygame.display.flip()

pygame.quit()