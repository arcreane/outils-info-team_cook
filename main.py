# main_weapons.py
import pygame, sys, random, os

# --- 1. CONFIGURATION DES CHEMINS ---
chemin_base = os.path.dirname(__file__)
dossiers = ['AllDatas', 'AllDatas/Entities', 'AllDatas/Weapons']
for dossier in dossiers:
    sys.path.append(os.path.abspath(os.path.join(chemin_base, dossier)))

# Imports des classes personnalisées (TES CODES)
from my_player import Player
from ennemi import Ennemi
from shoot import Shoot

# OPTIONNEL : si tu as power.py au bon endroit et importable
# Sinon on crée un petit Power local plus bas.
try:
    from power import Power
    POWER_OK = True
except Exception:
    POWER_OK = False


# ---------------------------
# Power local (si power.py pas importable)
# ---------------------------
if not POWER_OK:
    class Power(pygame.sprite.Sprite):
        def __init__(self, x, y, power_type="rapid"):
            super().__init__()
            self.image = pygame.Surface((30, 30))
            self.image.fill((255, 165, 0))
            self.rect = self.image.get_rect(topleft=(x, y))
            self.power_type = power_type
            self.vitesse = 2

        def update(self):
            self.rect.y += self.vitesse
            if self.rect.top > 600:
                self.kill()


# ---------------------------
# Weapon system (EXTERNE)
# ---------------------------
class WeaponManager:
    """
    Armes sans modifier Player/Shoot.
    weapon: normal | rapid | triple | big
    """
    def __init__(self):
        self.weapon = "normal"
        self.fire_delay = 200
        self.last_shot_time = 0

    def set_weapon(self, weapon_name: str):
        self.weapon = weapon_name

        if weapon_name == "normal":
            self.fire_delay = 200
        elif weapon_name == "rapid":
            self.fire_delay = 80
        elif weapon_name == "triple":
            self.fire_delay = 260
        elif weapon_name == "big":
            self.fire_delay = 350

    def try_shoot(self, joueur: Player, tous_les_sprites, groupe_tirs):
        temps_actuel = pygame.time.get_ticks()
        if temps_actuel - self.last_shot_time <= self.fire_delay:
            return

        self.last_shot_time = temps_actuel
        x = joueur.rect.centerx
        y = joueur.rect.top

        if self.weapon == "normal":
            tir = Shoot(x, y)
            tous_les_sprites.add(tir)
            groupe_tirs.add(tir)

        elif self.weapon == "rapid":
            tir = Shoot(x, y)
            tous_les_sprites.add(tir)
            groupe_tirs.add(tir)

        elif self.weapon == "triple":
            for offset in (-18, 0, 18):
                tir = Shoot(x + offset, y)
                tous_les_sprites.add(tir)
                groupe_tirs.add(tir)

        elif self.weapon == "big":
            tir = Shoot(x, y)
            # On adapte l'instance sans modifier shoot.py
            tir.vitesse = 7
            tir.image = pygame.transform.scale(tir.image, (20, 35))
            tir.rect = tir.image.get_rect()
            tir.rect.centerx = x
            tir.rect.bottom = y
            tous_les_sprites.add(tir)
            groupe_tirs.add(tir)


def apply_power(power_obj, weapon_mgr: WeaponManager):
    """
    Ton Player n'a pas fire_delay, donc on applique au WeaponManager.
    power_type possible : "rapid", "rapid_fire", "triple", "big", "big_fire"
    """
    t = getattr(power_obj, "power_type", "rapid")

    if t in ("rapid", "rapid_fire"):
        weapon_mgr.set_weapon("rapid")
    elif t in ("triple", "triple_fire"):
        weapon_mgr.set_weapon("triple")
    elif t in ("big", "big_fire"):
        weapon_mgr.set_weapon("big")
    else:
        weapon_mgr.set_weapon("normal")


# --- 2. INITIALISATION ---
pygame.init()
LARGEUR_ECRAN = 800
HAUTEUR_ECRAN = 600
ecran = pygame.display.set_mode((LARGEUR_ECRAN, HAUTEUR_ECRAN))
pygame.display.set_caption("Fireball Shoot 'em Up - Weapons Edition")
clock = pygame.time.Clock()
police = pygame.font.SysFont("Arial", 28)

# --- 3. GROUPES DE SPRITES ---
tous_les_sprites = pygame.sprite.Group()
groupe_ennemis = pygame.sprite.Group()
groupe_tirs = pygame.sprite.Group()
groupe_powers = pygame.sprite.Group()

# Création du joueur
joueur = Player()
tous_les_sprites.add(joueur)

# --- 4. VARIABLES DE JEU ---
score = 0
nombre_ennemis_max = 10

weapon_mgr = WeaponManager()  # <--- système d'armes

# Création initiale des ennemis
for _ in range(nombre_ennemis_max):
    e = Ennemi(random.randint(0, 750), random.randint(-400, -50))
    tous_les_sprites.add(e)
    groupe_ennemis.add(e)

# Timer spawn des powers
POWER_EVENT = pygame.USEREVENT + 1
pygame.time.set_timer(POWER_EVENT, 2500)  # toutes les 2.5 sec

# --- 5. BOUCLE DE JEU ---
running = True
while running:
    temps_actuel = pygame.time.get_ticks()

    # --- ÉVÉNEMENTS ---
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == POWER_EVENT:
            # spawn power aléatoire
            ptype = random.choice(["rapid_fire", "triple", "big_fire"])
            p = Power(random.randint(0, 770), -30, ptype)
            tous_les_sprites.add(p)
            groupe_powers.add(p)

    # --- LOGIQUE DE TIR (Maintien de la touche) ---
    touches = pygame.key.get_pressed()
    if touches[pygame.K_SPACE]:
        weapon_mgr.try_shoot(joueur, tous_les_sprites, groupe_tirs)

    # (optionnel) changer d'arme au clavier pour tester
    if touches[pygame.K_1]:
        weapon_mgr.set_weapon("normal")
    if touches[pygame.K_2]:
        weapon_mgr.set_weapon("rapid")
    if touches[pygame.K_3]:
        weapon_mgr.set_weapon("triple")
    if touches[pygame.K_4]:
        weapon_mgr.set_weapon("big")

    # --- MISE À JOUR ---
    tous_les_sprites.update()

    # --- COLLISIONS ---
    # Tirs / Ennemis
    hits = pygame.sprite.groupcollide(groupe_ennemis, groupe_tirs, True, True)
    for _ in hits:
        score += 10
        nouvel_e = Ennemi(random.randint(0, 750), random.randint(-150, -50))
        tous_les_sprites.add(nouvel_e)
        groupe_ennemis.add(nouvel_e)

    # Joueur / Power
    powers_ramasses = pygame.sprite.spritecollide(joueur, groupe_powers, True)
    for power_obj in powers_ramasses:
        apply_power(power_obj, weapon_mgr)

    # Ennemis / Joueur
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

    # --- DESSIN ET RENDU ---
    ecran.fill((30, 30, 30))
    tous_les_sprites.draw(ecran)

    # Interface (HUD)
    texte_score = police.render(f"SCORE: {score}", True, (255, 255, 255))
    texte_vies = police.render(f"VIES: {joueur.vie}", True, (255, 100, 100))
    texte_weapon = police.render(f"WEAPON: {weapon_mgr.weapon}", True, (180, 180, 255))

    ecran.blit(texte_score, (15, 15))
    ecran.blit(texte_vies, (15, 50))
    ecran.blit(texte_weapon, (15, 85))

    # Affichage "Invincible" (ton Player a invincible) :contentReference[oaicite:1]{index=1}
    if hasattr(joueur, 'invincible') and joueur.invincible:
        if (temps_actuel // 200) % 2 == 0:
            texte_inv = police.render("INVINCIBLE !", True, (255, 255, 0))
            ecran.blit(texte_inv, (630, 15))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
