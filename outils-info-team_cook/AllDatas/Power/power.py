import pygame
from AllDatas.Entities.entities import Entity


class Power(Entity):
    def __init__(self, x, y, power_type="rapid_fire"):
        super().__init__(x, y, 30, 30, (255, 165, 0), 1)
        self.power_type = power_type
        self.vitesse = 2

    def update(self):
        self.rect.y += self.vitesse
        if self.rect.top > 600:
            self.kill()

    def apply(self, player):
        if self.power_type == "rapid_fire":
            player.fire_delay = max(80, player.fire_delay - 100)
        else:
            player.big_fire = True

        self.kill()