from typing import Any
import pygame as pg
from pygame.math import Vector2
from components.particles import Particles

'''
  --- Enemy class ---
 This class is responsible for creating a sprite that follows other sprites.

  Functions:
    __init__ :
    update :
    on_draw :
    hurt_enemy :
'''

class Enemy(pg.sprite.Sprite):
  def __init__(self, player, pos, surf : pg.Surface, *groups):
    super().__init__(*groups)
    self.size = Vector2(10, 10)
    self.image = surf
    self.rect = self.image.get_rect(center=pos)
    self.pos = Vector2(pos)
    self.player = player


  def update_position(self):
    pass

  def update(self, dt):
    self.update_position()
