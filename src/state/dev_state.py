


import pygame as pg
from components.player import Player
from modules.state_machine import State

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


  # What is done on each frame when drawn
  def on_draw(self):
    self.engine.surface.fill((255, 255, 255))
    self.spites.draw(self.engine.surface)
    self.player.on_draw_player_sprites(self.engine.surface, None)

  # Updates relevant game state information
  def on_update(self, delta):
    self.dt = delta
    self.spites.update(delta)

  # Handles events (ie. key presses)
  def on_event(self, event):
    # Calls player's handle_event function (player's movements and attacks)
    self.player.handle_event(event=event, dt=self.dt)