import pygame, sys, random, os

# --- 1. CONFIGURATION DES CHEMINS ---
chemin_base = os.path.dirname(__file__)
dossiers = ['AllDatas', 'AllDatas/Entities', 'AllDatas/Weapons']
for dossier in dossiers:
    sys.path.append(os.path.abspath(os.path.join(chemin_base, dossier)))

# Imports des classes personnalisées
from player import Player
from ennemi import Ennemi
from shoot import Shoot

# --- 2. INITIALISATION ---
pygame.init()
LARGEUR_ECRAN = 800
HAUTEUR_ECRAN = 600
ecran = pygame.display.set_mode((LARGEUR_ECRAN, HAUTEUR_ECRAN))
pygame.display.set_caption("Fireball Shoot 'em Up - Ultra Edition")
clock = pygame.time.Clock()
police = pygame.font.SysFont("Arial", 28)

# --- 3. GROUPES DE SPRITES ---
tous_les_sprites = pygame.sprite.Group()
groupe_ennemis = pygame.sprite.Group()
groupe_tirs = pygame.sprite.Group()

# Création du joueur
joueur = Player()
tous_les_sprites.add(joueur)

# --- 4. VARIABLES DE JEU ---
score = 0
last_shot_time = 0
fire_delay = 200  # Vitesse de tir (ms)
nombre_ennemis_max = 10  # Ajusté pour que ce soit jouable (60 c'est énorme !)

# Création initiale des ennemis
for i in range(nombre_ennemis_max):
    e = Ennemi(random.randint(0, 750), random.randint(-400, -50))
    tous_les_sprites.add(e)
    groupe_ennemis.add(e)

# --- 5. BOUCLE DE JEU ---
running = True
while running:
    temps_actuel = pygame.time.get_ticks()

    # --- ÉVÉNEMENTS ---
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # --- LOGIQUE DE TIR (Maintien de la touche) ---
    touches = pygame.key.get_pressed()
    if touches[pygame.K_SPACE]:
        if temps_actuel - last_shot_time > fire_delay:
            tir = Shoot(joueur.rect.centerx, joueur.rect.top)
            tous_les_sprites.add(tir)
            groupe_tirs.add(tir)
            last_shot_time = temps_actuel

    # --- MISE À JOUR ---
    tous_les_sprites.update()

    # --- COLLISIONS ---
    # Tirs / Ennemis
    hits = pygame.sprite.groupcollide(groupe_ennemis, groupe_tirs, True, True)
    for hit in hits:
        score += 10
        nouvel_e = Ennemi(random.randint(0, 750), random.randint(-150, -50))
        tous_les_sprites.add(nouvel_e)
        groupe_ennemis.add(nouvel_e)

    # Ennemis / Joueur
    ennemis_touches = pygame.sprite.spritecollide(joueur, groupe_ennemis, True)
    if ennemis_touches:
        joueur.degat(1)
        # On fait réapparaître les ennemis qui ont touché le joueur
        for _ in ennemis_touches:
            nouvel_e = Ennemi(random.randint(0, 750), random.randint(-150, -50))
            tous_les_sprites.add(nouvel_e)
            groupe_ennemis.add(nouvel_e)

        if joueur.vie <= 0:
            print(f"GAME OVER ! Score final : {score}")
            running = False

    # --- DESSIN ET RENDU ---
    ecran.fill((30, 30, 30))  # Fond gris foncé

    tous_les_sprites.draw(ecran)

    # Interface (HUD)
    texte_score = police.render(f"SCORE: {score}", True, (255, 255, 255))
    texte_vies = police.render(f"VIES: {joueur.vie}", True, (255, 100, 100))
    ecran.blit(texte_score, (15, 15))
    ecran.blit(texte_vies, (15, 50))

    # Affichage "Invincible" si l'attribut existe dans ta classe Player
    if hasattr(joueur, 'invincible') and joueur.invincible:
        # Effet de clignotement
        if (temps_actuel // 200) % 2 == 0:
            texte_inv = police.render("INVINCIBLE !", True, (255, 255, 0))
            ecran.blit(texte_inv, (630, 15))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()