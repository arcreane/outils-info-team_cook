import pygame
from .entities import Entity

class Boss(Entity):
    def __init__(self):
        super().__init__(350, -100, 100, 80, (150, 0, 200), 50)
        self.vitesse_x = 3
        self.vitesse_y = 1
        self.last_shot = 0
        self.cible_y = 50

    def update(self):
        if self.rect.y < self.cible_y:
            self.rect.y += self.vitesse_y
        self.rect.x += self.vitesse_x
        if self.rect.right >= 800 or self.rect.left <= 0:
            self.vitesse_x *= -1

    def shoot(self, current_time):
        if current_time - self.last_shot > 1000:
            self.last_shot = current_time
            return [BossShoot(self.rect.left, self.rect.bottom),
                    BossShoot(self.rect.right, self.rect.bottom)]
        return []

class BossShoot(Entity):
    def __init__(self, x, y):
        super().__init__(x, y, 15, 15, (255, 0, 0), 1)
    def update(self):
        self.rect.y += 6
        if self.rect.top > 600: self.kill()