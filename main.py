import pygame, sys, os
from settings import *

# Gestion des chemins pour les modules personnalisés
chemin_base = os.path.dirname(__file__)
dossiers = ['AllDatas', 'AllDatas/Entities', 'AllDatas/Weapons']
for dossier in dossiers:
    sys.path.append(os.path.abspath(os.path.join(chemin_base, dossier)))

from game import Game


def main():
    pygame.init()
    ecran = pygame.display.set_mode((LARGEUR_ECRAN, HAUTEUR_ECRAN))
    pygame.display.set_caption("Shoot 'em Up - Boss Edition")
    clock = pygame.time.Clock()

    jeu = Game(ecran)

    while jeu.running:
        # Mécanique de Bullet Time : 20 FPS si Maj est pressé, sinon 60 FPS
        vitesse_actuelle = 20 if pygame.key.get_pressed()[pygame.K_LSHIFT] else FPS

        jeu.gerer_evenements()
        jeu.actualiser()
        jeu.dessiner()

        clock.tick(vitesse_actuelle)

    # Petit délai avant de quitter pour voir la victoire si nécessaire
    pygame.time.delay(1000)
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()