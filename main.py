import pygame, sys, random, os

# On ajoute tous les sous-dossiers au chemin de recherche de Python (j'ai cherché sur Internet pour ça - Nicolas)
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'AllDatas')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'AllDatas/Entities')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'AllDatas/Weapons')))

from player import Player
from ennemi import Ennemi
from shoot import Shoot

#création de la fenètre
pygame.init()
ecran = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Shoot Them Up")
clock = pygame.time.Clock()

#sprites gérer les entités
tous_les_sprites = pygame.sprite.Group()
groupe_ennemis = pygame.sprite.Group()
groupe_tirs = pygame.sprite.Group()


joueur = Player()
tous_les_sprites.add(joueur)

#60 ennemis avec spawn aléatoires
for i in range(60):
    e = Ennemi(random.randint(0, 750), random.randint(-300, 0))
    tous_les_sprites.add(e)
    groupe_ennemis.add(e)

# Variables de jeu
score = 0
font = pygame.font.Font(None, 36)

# Boucle principale du jeu
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            tir = Shoot(joueur.rect.centerx, joueur.rect.top)
            tous_les_sprites.add(tir)
            groupe_tirs.add(tir)

    tous_les_sprites.update()

    # Gestion des collisions entre tirs et ennemis
    collisions = pygame.sprite.groupcollide(groupe_ennemis, groupe_tirs, True, True)
    for ennemi in collisions:
        score += 10
        nouvel_ennemi = Ennemi(random.randint(0, 750), random.randint(-300, -40))
        tous_les_sprites.add(nouvel_ennemi)
        groupe_ennemis.add(nouvel_ennemi)

    # Gestion des collisions entre le joueur et les ennemis
    ennemis_touches = pygame.sprite.spritecollide(joueur, groupe_ennemis, True)
    if ennemis_touches:
        joueur.degat(1)
        for _ in ennemis_touches:
            nouvel_ennemi = Ennemi(random.randint(0, 750), random.randint(-300, -40))
            tous_les_sprites.add(nouvel_ennemi)
            groupe_ennemis.add(nouvel_ennemi)

        if joueur.vie <= 0:
            print(f"Game Over ! Score final : {score}")
            running = False

    ecran.fill((30, 30, 30))

    tous_les_sprites.draw(ecran)

    texte_score = font.render(f"Score: {score}", True, (255, 255, 255))
    texte_vies = font.render(f"Vies: {joueur.vie}", True, (255, 255, 255))
    ecran.blit(texte_score, (10, 10))
    ecran.blit(texte_vies, (10, 50))

    if joueur.invincible and joueur.temps_invincibilite % 10 < 5:
        texte_invincible = font.render("INVINCIBLE!", True, (255, 255, 0))
        ecran.blit(texte_invincible, (600, 550))

    pygame.display.flip()
    clock.tick(60)

#Quit Pygame
pygame.quit()
sys.exit()