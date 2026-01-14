import pygame
import random
from settings import *
from AllDatas.Entities.player import Player
from AllDatas.Entities.ennemi import Ennemi
from AllDatas.Entities.boss import Boss
from AllDatas.Weapons.weapon import WeaponManager, spawn_power


class Game:
    def __init__(self, ecran, image_fond):
        """Initialisation du jeu avec l'écran et l'image de fond JPG"""
        self.running = True
        self.ecran = ecran
        self.image_fond = image_fond  # Stockage de l'image de fond
        self.police = pygame.font.SysFont("Arial", 28)
        self.score = 0
        self.boss_mode = False
        self.boss = None

        # Gestionnaire d'armes
        self.weapon_manager = WeaponManager()

        # Groupes de sprites
        self.tous_les_sprites = pygame.sprite.Group()
        self.groupe_ennemis = pygame.sprite.Group()
        self.groupe_tirs = pygame.sprite.Group()
        self.groupe_tirs_boss = pygame.sprite.Group()
        self.groupe_powers = pygame.sprite.Group()

        # Initialisation du joueur
        self.joueur = Player()
        self.tous_les_sprites.add(self.joueur)

        # Apparition des premiers ennemis
        self.spawn_ennemis(NB_ENNEMIS_MAX)

    def spawn_ennemis(self, nombre):
        """Génère des ennemis à des positions aléatoires"""
        for _ in range(nombre):
            e = Ennemi(random.randint(0, LARGEUR_ECRAN - 40), random.randint(-400, -50))
            self.tous_les_sprites.add(e)
            self.groupe_ennemis.add(e)

    def gerer_evenements(self):
        """Gère les entrées clavier et la fermeture de la fenêtre"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

        touches = pygame.key.get_pressed()
        if touches[pygame.K_SPACE]:
            # Utilisation du WeaponManager pour gérer les différents types de tirs
            self.weapon_manager.try_shoot(self.joueur, self.tous_les_sprites, self.groupe_tirs)

    def actualiser(self):
        """Mise à jour de la logique du jeu (mouvements, collisions, spawn boss)"""
        # Activation du Boss si le score atteint 100
        if self.score >= 100 and not self.boss_mode:
            self.boss_mode = True
            for e in self.groupe_ennemis: e.kill()
            self.boss = Boss()
            self.tous_les_sprites.add(self.boss)

        # Mise à jour de la position de tous les éléments
        self.tous_les_sprites.update()

        # Logique spécifique au combat de Boss
        if self.boss_mode and self.boss:
            nouveaux_tirs = self.boss.shoot(pygame.time.get_ticks())
            for t in nouveaux_tirs:
                self.groupe_tirs_boss.add(t)
                self.tous_les_sprites.add(t)

            # Si le boss meurt, on arrête la partie (victoire)
            if self.boss.vie <= 0:
                self.groupe_tirs_boss.empty()
                self.running = False

        self.verifier_collisions()

        # Fin de partie si le joueur n'a plus de vie
        if self.joueur.vie <= 0:
            self.running = False

    def verifier_collisions(self):
        """Gère les interactions entre les différents groupes de sprites"""
        # Collecte de bonus (Power-ups)
        p_hits = pygame.sprite.spritecollide(self.joueur, self.groupe_powers, True)
        for p in p_hits:
            m = {"rapid_fire": "rapid", "triple": "triple", "big_fire": "big"}
            self.weapon_manager.set_weapon(m[p.power_type])

        # Tirs du joueur contre les ennemis classiques
        if not self.boss_mode:
            hits = pygame.sprite.groupcollide(self.groupe_ennemis, self.groupe_tirs, True, True)
            for _ in hits:
                self.score += 10
                self.spawn_ennemis(1)
                if random.random() < 0.2:  # Chance d'apparition d'un bonus
                    spawn_power(self.groupe_powers, self.tous_les_sprites)

        # Tirs du joueur contre le Boss
        elif self.boss:
            if pygame.sprite.spritecollide(self.boss, self.groupe_tirs, True):
                self.boss.degat(1)

        # Tirs du Boss contre le joueur
        if pygame.sprite.spritecollide(self.joueur, self.groupe_tirs_boss, True):
            self.joueur.degat(1)

        # Collision directe entre le joueur et les ennemis
        if pygame.sprite.spritecollide(self.joueur, self.groupe_ennemis, True):
            self.joueur.degat(1)
            if not self.boss_mode: self.spawn_ennemis(1)

    def dessiner(self):
        """Affiche les éléments sur l'écran"""
        # Affichage de l'image JPG personnalisée en fond
        self.ecran.blit(self.image_fond, (0, 0))

        # Dessin de tous les sprites (joueur, ennemis, tirs)
        self.tous_les_sprites.draw(self.ecran)

        # Affichage de l'interface (Score, Arme, Vies)
        self.afficher_hud()

        pygame.display.flip()

    def afficher_hud(self):
        """Affiche les informations de jeu en haut de l'écran"""
        txt_score = self.police.render(f"SCORE: {self.score} | ARME: {self.weapon_manager.weapon}", True, BLANC)
        txt_vies = self.police.render(f"VIES: {self.joueur.vie}", True, ROUGE_VIE)
        self.ecran.blit(txt_score, (15, 15))
        self.ecran.blit(txt_vies, (15, 50))