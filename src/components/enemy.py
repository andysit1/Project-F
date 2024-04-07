import pygame as pg
from pygame.math import Vector2

'''
  --- Enemy class ---
  This class is responsible for controlling everything about the enemies.
  (ie. enemy tracking, health, enemy attacks...)

  Functions:
    __init__ : Initializes the player object
    handle_event : Handles player events (ie. key presses)
    player_movement : Handles player directional movement
    update : Updates player information each frame/update
'''

class Enemy(pg.sprite.Sprite):
    def __init__(self, pos, *groups):
        super().__init__(*groups)
        self.image = pg.transform.scale(pg.image.load("./assets/fly.png").convert_alpha() , (40, 40))
        self.rect = self.image.get_rect(center=pos)
        self.pos = Vector2(pos)
        self.vel = Vector2(0, 0)
        self.speed = 400

def update(self):
        self.pos += self.vel
        self.rect.center = self.pos