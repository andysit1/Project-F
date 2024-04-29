import pygame
import random

'''
--- Particles class ---
This class is responsible for creating particles.
(ie. player dashes)

Functions:
  __init__ : Initializes the particles object
  generate_particles_frog_dash : Generates particles when the player dashes
  on_draw : Draws the particles

'''
#sprite object that holds particle effects
class Particles(pygame.sprite.Sprite):
  def __init__(self, player):
      super().__init__()
      self.player = player
      self.image = self.player.image
      self.rect = self.player.rect
      self.particles = []
      self.layer = 5

  def generate_particles_frog_dash(self):
      #generate 50 particles
      for _ in range(7):
        self.particles.append([[self.player.pos.x, self.player.pos.y + 30], [random.randint(0, 50) / 10 - 4, random.randint(-6, -3)], random.randint(1, 3), "white"])

  def generate_particles_blood(self):
      for _ in range(3):
        self.particles.append([[0, 0], [random.randint(0, 80) / 10 - 4, random.randint(-1, 1)], random.randint(1, 2), "red"])

  def update(self, dt):
      self.image = self.player.image.copy()
     #if particles exist then ...
      if len(self.particles) > 0:
        for particle in self.particles:
          print("hit")
          particle[0][0] += particle[1][0]
          particle[0][1] += particle[1][1]
          particle[2] -= 0.1
          particle[1][1] += 0.1
          pygame.draw.circle(self.image, particle[3], [int(particle[0][0]), int(particle[0][1])], int(particle[2]))
          if particle[2] <= 0:
              self.particles.remove(particle)
      else:
        self.kill()

#a generator that addes the particles into group
class ParticleGenerator():
  def __init__(self):
    self.image = None
    self.rect = None

  def generate_frog_dash_particles(self, focus):
     particle_obj = Particles(focus)
     particle_obj.generate_particles_frog_dash()
     return particle_obj

  def generate_blood_particles(self, focus):
     particle_obj = Particles(focus)
     particle_obj.generate_particles_blood()
     return particle_obj




