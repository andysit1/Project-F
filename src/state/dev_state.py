


import pygame as pg
from components.player import Player
from modules.state_machine import State

from components.attack import PierceGrappleAttack, AttackSprite
from components.attack import SweepAttackSprite

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

    #THIS must be moved to player since when map states are swaped we lose the group and our attacks box is lost
    # self.attack_sprite_test = PierceGrappleAttack(self.player, self.map_machine.current.group)
    self.attack_sprite_test = AttackSprite(self.player, self.spites)
    self.attack_sweep = SweepAttackSprite(self.player, self.spites)

  # What is done on each frame when drawn
  def on_draw(self):
    self.engine.surface.fill((255, 255, 255))
    self.spites.draw(self.engine.surface)

  # Updates relevant game state information
  def on_update(self, delta):
    self.dt = delta
    self.spites.update(delta)


  # Handles events (ie. key presses)
  def on_event(self, event):
    # Calls player's handle_event function (player's movements and attacks)
    self.player.handle_event(event=event, dt=self.dt)

    # If space is pressed, player attacks enemies
    if event.type == pg.KEYDOWN:
      if event.key == pg.K_SPACE:
        self.attack_sweep.handle_attack_input(self.enemy_group)
      elif event.key == pg.K_c:
        self.attack_sprite_test.perform_tongue(self.enemy_group)
      elif event.key == pg.K_0:
        self.dialogue_machine.current = True
      elif event.key == pg.K_9:
        self.on_swap_map_state()
      elif event.key == pg.K_ESCAPE:
        self.dialogue_engine.set_current(None)
