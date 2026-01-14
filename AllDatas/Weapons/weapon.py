# weapons.py
import pygame
import random
from shoot import Shoot

class Power(pygame.sprite.Sprite):

    def __init__(self, x, y, power_type="rapid_fire"):
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


class WeaponManager:

    def __init__(self):
        self.weapon = "normal"
        self.fire_delay = 200  # ms
        self.last_shot_time = 0


    def set_weapon(self, weapon_name):
        self.weapon = weapon_name

        if weapon_name == "normal":
            self.fire_delay = 200
        elif weapon_name == "rapid":
            self.fire_delay = 80
        elif weapon_name == "triple":
            self.fire_delay = 260
        elif weapon_name == "big":
            self.fire_delay = 350
        else:
            self.weapon = "normal"
            self.fire_delay = 200


    def try_shoot(self, player, all_sprites, bullets):
        now = pygame.time.get_ticks()
        if now - self.last_shot_time < self.fire_delay:
            return

        self.last_shot_time = now
        x = player.rect.centerx
        y = player.rect.top

        if self.weapon in ("normal", "rapid"):
            b = Shoot(x, y)
            all_sprites.add(b)
            bullets.add(b)

        elif self.weapon == "triple":
            for offset in (-18, 0, 18):
                b = Shoot(x + offset, y)
                all_sprites.add(b)
                bullets.add(b)

        elif self.weapon == "big":
            b = Shoot(x, y)
            b.vitesse = 7
            b.image = pygame.transform.scale(b.image, (20, 35))
            b.rect = b.image.get_rect()
            b.rect.centerx = x
            b.rect.bottom = y
            all_sprites.add(b)
            bullets.add(b)



def apply_power(power, weapon_manager: WeaponManager):

    if power.power_type == "rapid_fire":
        weapon_manager.set_weapon("rapid")

    elif power.power_type == "triple":
        weapon_manager.set_weapon("triple")

    elif power.power_type == "big_fire":
        weapon_manager.set_weapon("big")

    else:
        weapon_manager.set_weapon("normal")



def spawn_power(powers_group, all_sprites, width=800):

    power_type = random.choice(["rapid_fire", "triple", "big_fire"])
    p = Power(random.randint(0, width - 30), -30, power_type)
    powers_group.add(p)
    all_sprites.add(p)
