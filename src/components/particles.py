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

class Particles():
  def __init__(self, player):
      self.player = player
      self.particles = []

  def generate_particles_frog_dash(self):
      #generate 50 particles
      for _ in range(7):
        self.particles.append([[self.player.pos.x, self.player.pos.y + 30], [random.randint(0, 50) / 10 - 4, random.randint(-6, -3)], random.randint(1, 3)])

  def on_draw(self, surface):

     #if particles exist then ...
     if len(self.particles) > 0:
        for particle in self.particles:
          particle[0][0] += particle[1][0]
          particle[0][1] += particle[1][1]
          particle[2] -= 0.1
          particle[1][1] += 0.1
          pygame.draw.circle(surface, (255, 255, 255), [int(particle[0][0]), int(particle[0][1])], int(particle[2]))
          if particle[2] <= 0:
              self.particles.remove(particle)


