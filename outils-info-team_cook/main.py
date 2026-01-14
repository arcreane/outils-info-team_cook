import pygame, sys, os
from settings import *
# Gestion des chemins
chemin_base = os.path.dirname(__file__)
dossiers = ['AllDatas', 'AllDatas/Entities', 'AllDatas/Weapons', 'AllDatas/Assets']
for dossier in dossiers:
    sys.path.append(os.path.abspath(os.path.join(chemin_base, dossier)))

# Import du moteur de jeu après avoir configuré les chemins
from game import Game


def main():
    pygame.init()
    ecran = pygame.display.set_mode((LARGEUR_ECRAN, HAUTEUR_ECRAN))
    pygame.display.set_caption("Shoot 'em Up")
    clock = pygame.time.Clock()

    # Instance du jeu
    jeu = Game(ecran)

    # Boucle principale
    while jeu.running:
        jeu.gerer_evenements()
        jeu.actualiser()
        jeu.dessiner()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()

