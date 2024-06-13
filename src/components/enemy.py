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
  def __init__(self, player, pos, surf : pg.Surface, health, *groups):
    super().__init__(*groups)
    self.size = Vector2(10, 10)
    #import, load, and convert image to Surface, then scale it to 40x40
    self.image = surf
    self.rect = self.image.get_rect(center=pos)
    self.pos = Vector2(pos)
    self.vel = Vector2(0, 0)
    self.speed = 30
    self.max_health = health
    self.health = health
    self.player = player
    self.swallowable = False

    #particles
    self.enemy_particles = Particles(self)
    self.feet = pg.Rect(self.pos.x, self.pos.y, self.rect.width * 0.5, 8)


  def update_position(self):
    self.pos += self.vel
    self.rect.center = self.pos

  def update(self, dt):

    # Checks if enemy is swallowable
    if (self.health <= self.max_health/4):
      self.swallowable = True

    player_to_enemy_vector : pg.Vector2 = (self.player.pos - self.pos)
    is_enemy_in_range_of_player = player_to_enemy_vector.magnitude() < 300

    if (is_enemy_in_range_of_player):
      self.vel = player_to_enemy_vector.normalize() * self.speed * dt
    else:
      self.vel = (0,0)

    self.update_position()

  #need figure a work around as it's not drawing with the new map layout

  # # Hurts the enemy
  def hurt_enemy(self, damage):
    self.health -= damage

    knockback_velocity = (self.pos - self.player.pos).normalize() * 10
    self.vel = knockback_velocity

    self.update_position()


  #implement later...
  #this is supposed be a response to when enemies colide into the wall
  #I want a function to break the x, y and apply it seperately to the vel so it should still move down if we are moving diagonally
  def move_back(self, dt):
    pass




#Notes:
#instead of init a new healthbar surface each time we should init all possible surfaces healthbar surfaces into a dict in settings
#this way to reduce init cost of run time

#healthbar Sprite version.
class HealthBar(pg.sprite.Sprite):
  def __init__(self, focus : Enemy, *groups):
    super().__init__(*groups)

    #healthbar var variables
    self.feet = focus.feet
    self.size_bar_x = focus.size.x + 1
    self.size_bar_y = 2
    self.is_visible = False

    #entity variables...
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


  #helper functions -> abstract into a base entity class?
  def update_position(self):
    self.rect.center = self.focus.pos
    self.health = self.focus.health

  def make_transpart(self):
    self.is_visible = False
    self.image.set_alpha(0)

  def make_visible(self):
    self.is_visible = True
    self.image.set_alpha(255)


  def on_health_changes(self):
    if (self.health <= self.max_health/4):
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

    #concept: health bar should only appear when enemies are active
    is_same_position = self.old_pos == self.focus.pos
    is_different_health = self.old_health != self.health
    if is_same_position:
      self.make_transpart()
    else:
      self.make_visible()

    if is_different_health:
      self.on_health_changes()

    self.old_pos = self.focus.pos.copy()
    self.old_health = self.health
