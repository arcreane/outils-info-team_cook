import pygame, sys, random, os

#Trouve les fichiers en fonction de l'arborescence
chemin_base = os.path.dirname(__file__)
dossiers = ['AllDatas', 'AllDatas/Entities', 'AllDatas/Weapons']
for dossier in dossiers:
    sys.path.append(os.path.abspath(os.path.join(chemin_base, dossier)))

#Imports des classes créées
from player import Player
from ennemi import Ennemi
from shoot import Shoot

#Configuration de la page du jeu
pygame.init()
LARGEUR_ECRAN = 800
HAUTEUR_ECRAN = 600
ecran = pygame.display.set_mode((LARGEUR_ECRAN, HAUTEUR_ECRAN))
pygame.display.set_caption("Fireball Shoot 'em Up - Ultra Edition")
clock = pygame.time.Clock()
police = pygame.font.SysFont("Arial", 28)

#SPRITES
tous_les_sprites = pygame.sprite.Group()
groupe_ennemis = pygame.sprite.Group()
groupe_tirs = pygame.sprite.Group()

# Création du joueur
joueur = Player()
tous_les_sprites.add(joueur)

#Variable de jeu
score = 0
last_shot_time = 0
fire_delay = 200  #ms
nombre_ennemis_max = 10

# Création des ennemis
for i in range(nombre_ennemis_max):
    e = Ennemi(random.randint(0, 750), random.randint(-400, -50))
    tous_les_sprites.add(e)
    groupe_ennemis.add(e)

#Boucle de jeu
running = True
while running:
    temps_actuel = pygame.time.get_ticks()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    touches = pygame.key.get_pressed()
    if touches[pygame.K_SPACE]:
        if temps_actuel - last_shot_time > fire_delay:
            tir = Shoot(joueur.rect.centerx, joueur.rect.top)
            tous_les_sprites.add(tir)
            groupe_tirs.add(tir)
            last_shot_time = temps_actuel

    tous_les_sprites.update()

    #Collision system between shoot and mobs
    hits = pygame.sprite.groupcollide(groupe_ennemis, groupe_tirs, True, True)
    for hit in hits:
        score += 10
        nouvel_e = Ennemi(random.randint(0, 750), random.randint(-150, -50))
        tous_les_sprites.add(nouvel_e)
        groupe_ennemis.add(nouvel_e)

    #Collision system between player and mobs
    ennemis_touches = pygame.sprite.spritecollide(joueur, groupe_ennemis, True)
    if ennemis_touches:
        joueur.degat(1)
        for _ in ennemis_touches:
            nouvel_e = Ennemi(random.randint(0, 750), random.randint(-150, -50))
            tous_les_sprites.add(nouvel_e)
            groupe_ennemis.add(nouvel_e)

        if joueur.vie <= 0:
            print(f"GAME OVER ! Score final : {score}")
            running = False

    ecran.fill((30, 30, 30))  # Fond gris foncé

    tous_les_sprites.draw(ecran)

    #HUD à changer et à mettre dans menu/hud.py
    texte_score = police.render(f"SCORE: {score}", True, (255, 255, 255))
    texte_vies = police.render(f"VIES: {joueur.vie}", True, (255, 100, 100))
    ecran.blit(texte_score, (15, 15))
    ecran.blit(texte_vies, (15, 50))
    
    if hasattr(joueur, 'invincible') and joueur.invincible:
        # Effet de clignotement
        if (temps_actuel // 200) % 2 == 0:
            texte_inv = police.render("INVINCIBLE !", True, (255, 255, 0))
            ecran.blit(texte_inv, (630, 15))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()