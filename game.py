import pygame
import random
from settings import *
from player import Player
from ennemi import Ennemi


class Game:
    def __init__(self, ecran):
        self.ecran = ecran
        self.police = pygame.font.SysFont("Arial", 28)
        self.score = 0
        self.running = True

        # Groupes
        self.tous_les_sprites = pygame.sprite.Group()
        self.groupe_ennemis = pygame.sprite.Group()
        self.groupe_tirs = pygame.sprite.Group()

        # Joueur
        self.joueur = Player()
        self.tous_les_sprites.add(self.joueur)

        # Spawn initial
        self.spawn_ennemis(NB_ENNEMIS_MAX)

    def spawn_ennemis(self, nombre):
        for _ in range(nombre):
            e = Ennemi(random.randint(0, LARGEUR_ECRAN - 40), random.randint(-400, -50))
            self.tous_les_sprites.add(e)
            self.groupe_ennemis.add(e)

    def gerer_evenements(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

        # Logique de tir
        touches = pygame.key.get_pressed()
        if touches[pygame.K_SPACE]:
            tir = self.joueur.shoot(pygame.time.get_ticks())
            if tir:
                self.tous_les_sprites.add(tir)
                self.groupe_tirs.add(tir)

    def actualiser(self):
        self.tous_les_sprites.update()
        self.verifier_collisions()

        if self.joueur.vie <= 0:
            print(f"GAME OVER ! Score : {self.score}")
            self.running = False

    def verifier_collisions(self):
        # Tirs contre Ennemis
        hits = pygame.sprite.groupcollide(self.groupe_ennemis, self.groupe_tirs, True, True)
        for _ in hits:
            self.score += 10
            self.spawn_ennemis(1)

        # Joueur contre Ennemis
        touches = pygame.sprite.spritecollide(self.joueur, self.groupe_ennemis, True)
        if touches:
            self.joueur.degat(1)
            self.spawn_ennemis(len(touches))

    def dessiner(self):
        self.ecran.fill(COULEUR_FOND)
        self.tous_les_sprites.draw(self.ecran)
        self.afficher_hud()
        pygame.display.flip()

    def afficher_hud(self):
        txt_score = self.police.render(f"SCORE: {self.score}", True, BLANC)
        txt_vies = self.police.render(f"VIES: {self.joueur.vie}", True, ROUGE_VIE)
        self.ecran.blit(txt_score, (15, 15))
        self.ecran.blit(txt_vies, (15, 50))

        if self.joueur.invincible and (pygame.time.get_ticks() // 200) % 2 == 0:
            txt_inv = self.police.render("INVINCIBLE !", True, JAUNE_INV)
            self.ecran.blit(txt_inv, (630, 15))