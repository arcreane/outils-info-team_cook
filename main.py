import pygame, sys, os
from settings import *

# Gestion des chemins pour les modules personnalisés
chemin_base = os.path.dirname(__file__)
# Ajoutez '' pour inclure le dossier racine où se trouve settings.py
dossiers = ['', 'AllDatas', 'AllDatas/Entities', 'AllDatas/Weapons', 'AllDatas/Assets']
for dossier in dossiers:
    sys.path.append(os.path.abspath(os.path.join(chemin_base, dossier)))

from game import Game


def main():
    pygame.init()
    ecran = pygame.display.set_mode((LARGEUR_ECRAN, HAUTEUR_ECRAN))
    pygame.display.set_caption("Shoot 'em Up")
    clock = pygame.time.Clock()

    jeu = Game(ecran)

    while jeu.running:
        vitesse_actuelle = FPS

        jeu.gerer_evenements()
        jeu.actualiser()
        jeu.dessiner()

        clock.tick(vitesse_actuelle)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
