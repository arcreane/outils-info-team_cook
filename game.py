import pygame
import random
from settings import *
from AllDatas.Entities.player import Player
from AllDatas.Entities.ennemi import Ennemi
from AllDatas.Entities.boss import Boss
from AllDatas.Weapons.weapon import WeaponManager, spawn_power

class Game:
    def __init__(self, ecran):
        self.running = True
        self.ecran = ecran
        self.score = 0
        self.boss_mode = False
        self.boss = None
        self.weapon_manager = WeaponManager()
        self.police = pygame.font.SysFont("Arial", 28)

        self.tous_les_sprites = pygame.sprite.Group()
        self.groupe_ennemis = pygame.sprite.Group()
        self.groupe_tirs = pygame.sprite.Group()
        self.groupe_tirs_boss = pygame.sprite.Group()
        self.groupe_powers = pygame.sprite.Group()

        self.joueur = Player()
        self.tous_les_sprites.add(self.joueur)
        self.spawn_ennemis(NB_ENNEMIS_MAX) # Méthode maintenant définie

    def spawn_ennemis(self, nombre):
        for _ in range(nombre):
            e = Ennemi(random.randint(0, LARGEUR_ECRAN - 40), random.randint(-400, -50))
            self.tous_les_sprites.add(e)
            self.groupe_ennemis.add(e)

    def gerer_evenements(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT: self.running = False
        if pygame.key.get_pressed()[pygame.K_SPACE]:
            self.weapon_manager.try_shoot(self.joueur, self.tous_les_sprites, self.groupe_tirs)

    def actualiser(self):
        if self.score >= 100 and not self.boss_mode:
            self.boss_mode = True
            for e in self.groupe_ennemis: e.kill()
            self.boss = Boss(); self.tous_les_sprites.add(self.boss)

        self.tous_les_sprites.update()
        if self.boss_mode and self.boss:
            tirs = self.boss.shoot(pygame.time.get_ticks())
            for t in tirs: self.groupe_tirs_boss.add(t); self.tous_les_sprites.add(t)

        self.verifier_collisions()
        if self.joueur.vie <= 0: self.running = False

    def verifier_collisions(self):
        # Power-ups
        hits = pygame.sprite.spritecollide(self.joueur, self.groupe_powers, True)
        for p in hits:
            m = {"rapid_fire": "rapid", "triple": "triple", "big_fire": "big"}
            self.weapon_manager.set_weapon(m[p.power_type])

        # Tirs joueur vs Ennemis/Boss
        if not self.boss_mode:
            hits = pygame.sprite.groupcollide(self.groupe_ennemis, self.groupe_tirs, True, True)
            for _ in hits:
                self.score += 10; self.spawn_ennemis(1)
                if random.random() < 0.2: spawn_power(self.groupe_powers, self.tous_les_sprites)
        elif self.boss:
            if pygame.sprite.spritecollide(self.boss, self.groupe_tirs, True):
                self.boss.degat(1)

        # Tirs Boss vs Joueur
        if pygame.sprite.spritecollide(self.joueur, self.groupe_tirs_boss, True):
            self.joueur.degat(1)

    def dessiner(self):
        self.ecran.fill(COULEUR_FOND)
        self.tous_les_sprites.draw(self.ecran)
        self.afficher_hud()
        pygame.display.flip()

    def afficher_hud(self):
        s_txt = self.police.render(f"SCORE: {self.score} | ARME: {self.weapon_manager.weapon}", True, BLANC)
        self.ecran.blit(s_txt, (15, 15))
        v_txt = self.police.render(f"VIES: {self.joueur.vie}", True, ROUGE_VIE)
        self.ecran.blit(v_txt, (15, 50))