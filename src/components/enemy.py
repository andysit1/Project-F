from typing import Any
import pygame as pg
from pygame.math import Vector2
from components.player import Player
from components.particles import Particles
from settings import Settings
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
  def __init__(self, player : Player, pos, surf : pg.Surface, health, *groups):
    super().__init__(*groups)
    settings = Settings()
    self.size = Vector2(40, 40)
    #import, load, and convert image to Surface, then scale it to 40x40
    self.image = surf
    self.rect = self.image.get_rect(center=pos)
    self.pos = Vector2(pos)
    self.vel = Vector2(0, 0)
    self.speed = 40
    self.max_health = health
    self.health = health
    self.player = player
    self.swallowable = False

    #particles
    self.enemy_particles = Particles(self)
    self.feet = pg.Rect(self.pos.x, self.pos.y, self.rect.width * 0.5, 8)


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

    # Updates position of enemy
    self.pos += self.vel
    self.rect.center = self.pos


  #need figure a work around as it's not drawing with the new map layout

  # # Hurts the enemy
  def hurt_enemy(self, damage):
    self.health -= damage
    # Generate blood particles
    self.enemy_particles.generate_particles_blood()
    # Knockback effect
    if (self.pos - self.player.pos).magnitude() != 0:
      self.vel = (self.pos - self.player.pos).normalize() * 10 # <- Knockback amount

      # Updates position of enemy
      self.pos += self.vel
      self.rect.center = self.pos

  #implement later...
  #this is supposed be a response to when enemies colide into the wall
  def move_back(self, dt):
    pass


#instead of init a new healthbar surface each time we should init all possible surfaces healthbar surfaces into a dict in settings 
#this way to reduce init cost of run time



#healthbar Sprite version. 
class HealthBar(pg.sprite.Sprite):
  def __init__(self, focus : Enemy, *groups):
    super().__init__(*groups)

    #healthbar var variables
    self.feet = focus.feet
    self.size_bar_x = focus.size.x + 4
    self.size_bar_y = 7
    self.is_visible = False

    #entity variables...
    self.focus = focus
    self.old_pos = None
    self.health = focus.health
    self.max_health = focus.max_health
    self.swallowable = False


    self.move_back = focus.move_back
    #visual variables...
    self.image = pg.Surface([self.size_bar_x, self.size_bar_y])
    self.image.fill("red")
    self.image.set_alpha(0)
    self.rect = self.image.get_rect(center=self.focus.pos)


  def update(self, dt):

    #update the positions and health
    self.rect.center = self.focus.pos
    self.health = self.focus.health

    #if moved then we know it is in range
    if self.old_pos == self.focus.pos:
      self.is_visible = False
      self.image.set_alpha(0)  #make transparent
    else:
      self.is_visible = True
      self.image.set_alpha(255) #make not transparent


    if self.is_visible:
      if (self.health <= self.max_health/4):
            self.swallowable = True
            self.image.fill("yellow")

      if self.health < 0:
        self.focus.kill()
        self.kill()

      #is there a way to not have to run this each iteration to improve performance
      #not sure if it matters since it's constant and not a loop but still transforming seems to be an resource intensive function
      try:
        #resizes the image base on remaining health
        self.image = pg.transform.scale(self.image, [self.size_bar_x * (self.health / self.max_health), self.size_bar_y])
      except:
        pass

    self.old_pos = self.focus.pos.copy()



# def draw(self, surface : pg.Surface):
#   # Draws the enemy
#   surface.blit(self.image, self.rect.topleft)
#   self.enemy_particles.on_draw(surface)
#   # Draws the health bar above the enemy
#   if ((self.pos - self.player.pos).magnitude() < 300):
#     pg.draw.rect(surface, "black", (self.pos.x - self.size.x/2 - 2, self.pos.y - self.size.y/2 - 6, self.size.x + 4, 7))
#     # Draws the health bar yellow if the enemy is swallowable
#     if(self.swallowable):
#       pg.draw.rect(surface, "yellow", (self.pos.x - self.size.x/2, self.pos.y - self.size.y/2 - 5, (self.health / self.max_health) * self.size.x, 5))
#     else:
#       pg.draw.rect(surface, "red", (self.pos.x - self.size.x/2, self.pos.y - self.size.y/2 - 5, (self.health / self.max_health) * self.size.x, 5))
