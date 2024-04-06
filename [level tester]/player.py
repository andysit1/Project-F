from random import randrange

import pygame as pg
from pygame.math import Vector2

class Player(pg.sprite.Sprite):

    def __init__(self, pos, *groups):
        super().__init__(*groups)
        self.image = pg.Surface((30, 30))
        self.image.fill(pg.Color('red'))
        self.rect = self.image.get_rect(center=pos)
        self.pos = Vector2(pos)
        self.vel = Vector2(0, 0)
        self.speed = 4

    def input(self, event):
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_d:
                self.vel.x = self.speed
            elif event.key == pg.K_a:
                self.vel.x = -self.speed
            elif event.key == pg.K_w:
                self.vel.y = -self.speed
            elif event.key == pg.K_s:
                self.vel.y = self.speed
        elif event.type == pg.KEYUP:
            if event.key == pg.K_d and self.vel.x > 0:
                self.vel.x = 0
            elif event.key == pg.K_a and self.vel.x < 0:
                self.vel.x = 0
            elif event.key == pg.K_w and self.vel.y < 0:
                self.vel.y = 0
            elif event.key == pg.K_s and self.vel.y > 0:
                self.vel.y = 0

    def update(self):
        # Move the player.
        self.pos += self.vel
        self.rect.center = self.pos