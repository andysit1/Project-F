


import pygame as pg
from components.player import Player
from modules.lighting_manager import LightingManager, circle_surf
from modules.state_machine import State
import random

'''
  --- GameState class ---
  This class is responsible for managing the game state, which includes everything currently loaded into the game.
  (ie. everything not in the main menu, settings...)
  (ie. the player, enemies, background...)

  Functions:
    __init__ : Initializes the game state
    on_draw : Draws the game state
    on_event : Handles game state events (ie. key presses)
    on_update : Updates game state information each frame/update
'''

class DevState(State):
  def __init__(self, engine):
    super().__init__(engine)
    self.engine = engine
    self.spites : pg.sprite.Group = pg.sprite.Group()
    self.player = Player((40, 40), self.spites)
    self.dt = None

    # [loc, velocity, timer]
    self.particles = []
    self.glow_rects : list[pg.Rect] = [pg.Rect(100, 100, 30, 30), pg.Rect(90, 110, 30, 30)]
    self.light_manager = LightingManager()
    # self.light_manager.set_glow_objects(self.glow_rects)


  def draw_test_rects(self):
    return [pg.draw.rect(self.engine.surface, "BLUE", rect=rect) for rect in self.glow_rects]
  # What is done on each frame when drawn


  def update_glow_particles(self):
    mx, my = pg.mouse.get_pos()
    self.particles.append([[mx, my], [random.randint(0, 20) / 10 - 1, -5], random.randint(6, 11)])

    for particle in self.particles:
      particle[0][0] += particle[1][0]
      particle[0][1] += particle[1][1]
      particle[2] -= 0.1
      particle[1][1] += 0.15

      #particle timer is over remove
      if particle[2] <= 0:
          self.particles.remove(particle)

  def on_draw(self):
      self.engine.surface.fill((0,0,0))
      #game
      self.spites.draw(self.engine.surface)
      self.player.on_draw_player_sprites(self.engine.surface, None)

      if self.particles:
        self.light_manager.draw(self.engine.surface, self.particles)

  # self.light_manager.draw(self.engine.surface)
  # Updates relevant game state information
  def on_update(self, delta):
    self.dt = delta
    self.spites.update(delta)
    self.update_glow_particles()

  # Handles events (ie. key presses)
  def on_event(self, event):
    # Calls player's handle_event function (player's movements and attacks)
    self.player.handle_event(event=event, dt=self.dt)