import pygame, sys, os
from settings import *

<<<<<<< HEAD
# Gestion des chemins pour les modules personnalisés
chemin_base = os.path.dirname(__file__)
# Ajoutez '' pour inclure le dossier racine où se trouve settings.py
=======
chemin_base = os.path.dirname(__file__)
>>>>>>> PresentaionTom
dossiers = ['', 'AllDatas', 'AllDatas/Entities', 'AllDatas/Weapons', 'AllDatas/Assets']
for dossier in dossiers:
    sys.path.append(os.path.abspath(os.path.join(chemin_base, dossier)))

from game import Game


<<<<<<< HEAD
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
=======
def afficher_menu(ecran, fond):
    police_titre = pygame.font.SysFont("Arial", 80, bold=True)
    police_bouton = pygame.font.SysFont("Arial", 40, bold=True)

    en_menu = True
    while en_menu:
        # On dessine ton image de fond personnalisée
        ecran.blit(fond, (0, 0))

        souris = pygame.mouse.get_pos()
        txt_titre = "Shoot 'em Up"

        # Titre
        texte_titre = police_titre.render(txt_titre, True, BLANC)
        rect_titre = texte_titre.get_rect(center=(LARGEUR_ECRAN // 2, HAUTEUR_ECRAN // 3))
        ecran.blit(texte_titre, rect_titre)

        # Bouton JOUER
        rect_bouton = pygame.Rect(0, 0, 250, 70)
        rect_bouton.center = (LARGEUR_ECRAN // 2, HAUTEUR_ECRAN // 2 + 50)
        sur_bouton = rect_bouton.collidepoint(souris)

        couleur_btn = (0, 200, 0) if sur_bouton else (0, 150, 0)
        pygame.draw.rect(ecran, (255, 255, 255), rect_bouton.inflate(5 if sur_bouton else 0, 5 if sur_bouton else 0),
                         border_radius=15)
        pygame.draw.rect(ecran, couleur_btn, rect_bouton.inflate(-4, -4), border_radius=12)

        img_jouer = police_bouton.render("JOUER", True, BLANC)
        ecran.blit(img_jouer, img_jouer.get_rect(center=rect_bouton.center))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and rect_bouton.collidepoint(event.pos):
                en_menu = False


def main():
    pygame.init()
    ecran = pygame.display.set_mode((LARGEUR_ECRAN, HAUTEUR_ECRAN))
    clock = pygame.time.Clock()

    # Chargement de ton image .jpg
    try:
        img_fond = pygame.image.load(IMAGE_FOND).convert()
        img_fond = pygame.transform.scale(img_fond, (LARGEUR_ECRAN, HAUTEUR_ECRAN))
    except Exception as e:
        print(f"Erreur chargement fond: {e}")
        # Fond de secours si l'image est introuvable
        img_fond = pygame.Surface((LARGEUR_ECRAN, HAUTEUR_ECRAN))
        img_fond.fill(COULEUR_FOND)

    afficher_menu(ecran, img_fond)

    jeu = Game(ecran, img_fond)

    while jeu.running:
        jeu.gerer_evenements()
        jeu.actualiser()
        jeu.dessiner()
        clock.tick(FPS)
>>>>>>> PresentaionTom

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
<<<<<<< HEAD
    main()
=======
    main()
>>>>>>> PresentaionTom
