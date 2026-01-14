import pygame
import random
from settings import *
from AllDatas.Entities.player import Player
from AllDatas.Entities.ennemi import Ennemi
from AllDatas.Entities.boss import Boss  # Import du Boss
from AllDatas.Weapons.weapon import WeaponManager, spawn_power  # Import du Manager


class Game:
    def __init__(self, ecran):
        self.running = True  # Toujours en premier
        self.ecran = ecran
        self.police = pygame.font.SysFont("Arial", 28)
        self.score = 0
        self.boss_mode = False
        self.boss = None

        # Gestionnaire d'armes
        self.weapon_manager = WeaponManager()

        # Groupes
        self.tous_les_sprites = pygame.sprite.Group()
        self.groupe_ennemis = pygame.sprite.Group()
        self.groupe_tirs = pygame.sprite.Group()
        self.groupe_tirs_boss = pygame.sprite.Group()  # Nouveau groupe
        self.groupe_powers = pygame.sprite.Group()  # Nouveau groupe

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

        touches = pygame.key.get_pressed()
        if touches[pygame.K_SPACE]:
            # Utilisation du WeaponManager pour le tir du joueur
            self.weapon_manager.try_shoot(self.joueur, self.tous_les_sprites, self.groupe_tirs)

    def actualiser(self):
        # Activation du Boss à 100 points
        if self.score >= 100 and not self.boss_mode:
            self.boss_mode = True
            for e in self.groupe_ennemis: e.kill()
            self.boss = Boss()
            self.tous_les_sprites.add(self.boss)

        # Update de tous les sprites
        self.tous_les_sprites.update()

        # Logique spécifique au Boss
        if self.boss_mode and self.boss:
            # COMMANDE DE TIR DU BOSS
            nouveaux_tirs = self.boss.shoot(pygame.time.get_ticks())
            for t in nouveaux_tirs:
                self.groupe_tirs_boss.add(t)
                self.tous_les_sprites.add(t)

            # Vérification mort du Boss
            if self.boss.vie <= 0:
                self.groupe_tirs_boss.empty()  # Nettoyage des projectiles restants
                self.running = False

        self.verifier_collisions()

        if self.joueur.vie <= 0:
            self.running = False

    def verifier_collisions(self):
        # Joueur contre Power-ups
        p_hits = pygame.sprite.spritecollide(self.joueur, self.groupe_powers, True)
        for p in p_hits:
            m = {"rapid_fire": "rapid", "triple": "triple", "big_fire": "big"}
            self.weapon_manager.set_weapon(m[p.power_type])

        # Tirs contre Ennemis (si pas en mode boss)
        if not self.boss_mode:
            hits = pygame.sprite.groupcollide(self.groupe_ennemis, self.groupe_tirs, True, True)
            for _ in hits:
                self.score += 10
                self.spawn_ennemis(1)
                if random.random() < 0.2:  # 20% de chance de bonus
                    spawn_power(self.groupe_powers, self.tous_les_sprites)

        # Tirs contre Boss
        elif self.boss:
            if pygame.sprite.spritecollide(self.boss, self.groupe_tirs, True):
                self.boss.degat(1)

        # Tirs Boss contre Joueur
        if pygame.sprite.spritecollide(self.joueur, self.groupe_tirs_boss, True):
            self.joueur.degat(1)

        # Joueur contre Ennemis
        if pygame.sprite.spritecollide(self.joueur, self.groupe_ennemis, True):
            self.joueur.degat(1)
            if not self.boss_mode: self.spawn_ennemis(1)

    def dessiner(self):
        self.ecran.fill(COULEUR_FOND)
        self.tous_les_sprites.draw(self.ecran)
        self.afficher_hud()
        pygame.display.flip()

    def afficher_hud(self):
        txt_score = self.police.render(f"SCORE: {self.score} | ARME: {self.weapon_manager.weapon}", True, BLANC)
        txt_vies = self.police.render(f"VIES: {self.joueur.vie}", True, ROUGE_VIE)
        self.ecran.blit(txt_score, (15, 15))
        self.ecran.blit(txt_vies, (15, 50))