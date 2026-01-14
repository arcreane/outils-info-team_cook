import pygame
import random
from AllDatas.Entities.player import Shoot

class Power(pygame.sprite.Sprite):
    def __init__(self, x, y, power_type="rapid_fire"):
        super().__init__()
        self.image = pygame.Surface((30, 30))
        couleurs = {"rapid_fire": (255, 165, 0), "triple": (0, 255, 255), "big_fire": (255, 0, 255)}
        self.image.fill(couleurs.get(power_type, (255, 255, 255)))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.power_type = power_type
        self.vitesse = 2

    def update(self):
        self.rect.y += self.vitesse
        if self.rect.top > 600:
            self.kill()

class WeaponManager:
    def __init__(self):
        self.weapon = "normal"
        self.fire_delay = 200
        self.last_shot_time = 0

    def set_weapon(self, weapon_name):
        self.weapon = weapon_name
        stats = {"normal": 200, "rapid": 80, "triple": 260, "big": 350}
        self.fire_delay = stats.get(weapon_name, 200)

    def try_shoot(self, player, all_sprites, bullets):
        now = pygame.time.get_ticks()
        if now - self.last_shot_time < self.fire_delay:
            return

        self.last_shot_time = now
        x, y = player.rect.centerx, player.rect.top

        if self.weapon in ("normal", "rapid"):
            b = Shoot(x, y)
            all_sprites.add(b); bullets.add(b)
        elif self.weapon == "triple":
            for offset in (-20, 0, 20):
                b = Shoot(x + offset, y)
                all_sprites.add(b); bullets.add(b)
        elif self.weapon == "big":
            b = Shoot(x, y)
            b.vitesse = 7
            b.image = pygame.transform.scale(b.image, (40, 60))
            b.rect = b.image.get_rect(centerx=x, bottom=y)
            all_sprites.add(b); bullets.add(b)

def spawn_power(powers_group, all_sprites, width=800):
    p_type = random.choice(["rapid_fire", "triple", "big_fire"])
    p = Power(random.randint(0, width - 30), -30, p_type)
    powers_group.add(p); all_sprites.add(p)