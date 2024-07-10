from typing import Any
import pygame as pg
from pygame.math import Vector2
from components.particles import Particles

'''
  --- Enemy class ---
  This class is responsible for controlling everything about the enemies.
  (ie. enemy tracking, health, enemy attacks...)

  Functions:
    __init__ : Initializes the enemy object
    update : Updates enemy information each frame, like movement
    on_draw : Draws all of the enemies graphics
    hurt_enemy : When the enemy is hurt, lowers health and knockback
'''

class Enemy(pg.sprite.Sprite):
  def __init__(self, player, pos, surf : pg.Surface, health, speed, *groups):
    super().__init__(*groups)
    self.size = Vector2(10, 10)
    self.image = surf
    self.rect = self.image.get_rect(center=pos)
    self.pos = Vector2(pos)
    self.vel = Vector2(0, 0)
    self.speed = speed
    self.max_health = health
    self.health = health
    self.player = player
    self.swallowable = False

    # particles
    self.enemy_particles = Particles(self)
    self.feet = pg.Rect(self.pos.x, self.pos.y, self.rect.width * 0.5, 8)

  def update_position(self):
    self.pos += self.vel
    self.rect.center = self.pos

  def update(self, dt):

    # Checks if enemy is swallowable
    if self.health <= self.max_health / 4:
      self.swallowable = True

    # Moves enemy to player, if in range
    player_to_enemy_vector = self.player.pos - self.pos
    player_distance = player_to_enemy_vector.magnitude()
    if 10 < player_distance < 200:
      self.vel = player_to_enemy_vector.normalize() * self.speed * dt
    else:
      self.vel = Vector2(0, 0)

    # Moves enemies away from each other, if in range
    for sprite in self.groups()[0]:
      if sprite is not self and sprite.__class__.__name__ == "Enemy":
        enemy_to_enemy_vector = sprite.pos - self.pos
        enemy_distance = enemy_to_enemy_vector.magnitude() 
        if enemy_distance < 10:
          self.vel -= enemy_to_enemy_vector.normalize() * self.speed * dt

    self.update_position()

  def hurt_enemy(self, damage):
    self.health -= damage
    knockback_velocity = (self.pos - self.player.pos).normalize() * 10
    self.vel = knockback_velocity
    self.update_position()

  def move_back(self, dt):
    pass

class HealthBar(pg.sprite.Sprite):
  def __init__(self, focus: Enemy, *groups):
    super().__init__(*groups)
    self.feet = focus.feet
    self.size_bar_x = focus.size.x + 1
    self.size_bar_y = 2
    self.is_visible = False

    self.focus = focus
    self.old_pos = None
    self.health = focus.health
    self.old_health = None
    self.max_health = focus.max_health
    self.swallowable = False

    self.move_back = focus.move_back
    
    #visual variables...
    self.image = pg.Surface([self.size_bar_x, self.size_bar_y])
    self.image.fill("red")
    self.image.set_alpha(0)
    self.rect = self.image.get_rect(center=self.focus.pos)

  def update_position(self):
    self.rect.center = self.focus.pos
    self.health = self.focus.health

  def make_transparent(self):
    self.is_visible = False
    self.image.set_alpha(0)

  def make_visible(self):
    self.is_visible = True
    self.image.set_alpha(255)

  def on_health_changes(self):
    if self.health <= self.max_health / 4:
      self.swallowable = True
      self.image.fill("yellow")

    if self.health < 0:
      self.focus.kill()
      self.kill()

    health_to_maxhealth_ratio = self.size_bar_x * (self.health / self.max_health)
    try:
      self.image = pg.transform.scale(self.image, [health_to_maxhealth_ratio, self.size_bar_y])
    except:
      pass
    
  def hurt_enemy(self, damage):
    self.health -= damage

  def update(self, dt):
    self.update_position()

    is_same_position = self.old_pos == self.focus.pos
    is_different_health = self.old_health != self.health
    if is_same_position:
      self.make_transparent()
    else:
      self.make_visible()

    if is_different_health:
      self.on_health_changes()

    self.old_pos = self.focus.pos.copy()
    self.old_health = self.health
