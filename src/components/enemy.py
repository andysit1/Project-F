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
  def __init__(self, pos, img_name, *groups):
    super().__init__(*groups)
    #import, load, and convert image to Surface, then scale it to 40x40
    self.image = pg.transform.scale(pg.image.load("./assets/" + img_name + ".png").convert_alpha() , (40, 40))
    self.rect = self.image.get_rect(center=pos)
    self.pos = Vector2(pos)
    self.vel = Vector2(0, 0)
    self.speed = 40

  def update(self, Player, dt):

    # If the player is within 300 pixels of the enemy, the enemy will move towards the player
    if ((self.pos - Player.pos).magnitude() < 300):
      self.vel = (Player.pos - self.pos).normalize() * self.speed * dt
    else:
      self.vel = Vector2(0, 0)

    # Updates position of enemy
    self.pos += self.vel
    self.rect.center = self.pos


        