import pygame
import sys
import random 


from AllDatas.player import Player
from AllDatas.ennemi import Ennemi
# Configuration de base
pygame.init()
ecran = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()

tous_les_sprites = pygame.sprite.Group()
groupe_ennemis = pygame.sprite.Group()

# Création des objets
joueur = Player()
tous_les_sprites.add(joueur)

for i in range(5):
    e = Ennemi(i * 150, 50)
    tous_les_sprites.add(e)
    groupe_ennemis.add(e)

# Boucle principale
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    tous_les_sprites.update()
    ecran.fill((30, 30, 30)) # Gris foncé
    tous_les_sprites.draw(ecran)
    
    pygame.display.flip()
    clock.tick(60) # Limite à 60 FPS
