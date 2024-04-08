import pygame as pg
from pygame.math import Vector2
from components.player import Player
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
  def __init__(self, player : Player, pos, img_name, health, *groups):
    super().__init__(*groups)
    self.size = Vector2(40, 40)
    #import, load, and convert image to Surface, then scale it to 40x40
    self.image = pg.transform.scale(pg.image.load("./assets/" + img_name + ".png").convert_alpha() , (self.size.x, self.size.y))
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

  def update(self, dt, surface : pg.Surface):

    # Checks if enemy is swallowable
    if (self.health <= self.max_health/4):
      self.swallowable = True

    # If the player is within 300 pixels of the enemy, the enemy will move towards the player
    if ((self.pos - self.player.pos).magnitude() < 300):
      self.vel = (self.player.pos - self.pos).normalize() * self.speed * dt
    else:
      self.vel = Vector2(0, 0)

    # Updates position of enemy
    self.pos += self.vel
    self.rect.center = self.pos

  def on_draw(self, surface : pg.Surface):
    # Draws the enemy
    surface.blit(self.image, self.rect.topleft)
    self.enemy_particles.on_draw(surface)
    # Draws the health bar above the enemy
    if ((self.pos - self.player.pos).magnitude() < 300):
      pg.draw.rect(surface, "black", (self.pos.x - self.size.x/2 - 2, self.pos.y - self.size.y/2 - 6, self.size.x + 4, 7))
      # Draws the health bar yellow if the enemy is swallowable
      if(self.swallowable):
        pg.draw.rect(surface, "yellow", (self.pos.x - self.size.x/2, self.pos.y - self.size.y/2 - 5, (self.health / self.max_health) * self.size.x, 5))
      else:
        pg.draw.rect(surface, "red", (self.pos.x - self.size.x/2, self.pos.y - self.size.y/2 - 5, (self.health / self.max_health) * self.size.x, 5))

  # Hurts the enemy
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