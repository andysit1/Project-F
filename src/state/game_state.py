import pygame as pg
from random import randrange
from pygame.math import Vector2
from modules.state_machine import State, Machine
from components.player import Player
from components.enemy import Enemy, HealthBar
from components.ui import Interface
from components.dialogue import Dialogue, DialogueDisplayEngine, DialogueState
from components.camera import Camera
from settings import Settings, MapSettings
from components.particles import ParticleGenerator
from components.attack import AttackSprite
from components.attack import SweepAttackSprite
from modules.state_machine import Machine

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

class GameState(State):
  def __init__(self, engine):
    super().__init__(engine)
    self.settings = Settings()               #init pygame surfaces

    self.dt = 0                              # Initializes delta time
    self.clock = pg.time.Clock()             # Needed clock thing?
    font = pg.font.SysFont('comicsans', 15)  # Initializes font

    self.map_settings = MapSettings()        #init map settings
    self.map_machine = Machine()
    self.map_machine.current = self.map_settings.maps.get("base") #set the first state as base

    self.player = self.map_machine.current.player
    self.enemy_group = self.map_machine.current.enemy_grp

    self.ui = Interface(self.player)
    self.camera_view = Camera(self.player)
    self.particle_gen = ParticleGenerator()

    self.attack_sprite_test = AttackSprite(self.player, self.map_machine.current.group)
    self.attack_sweep = SweepAttackSprite(self.player, self.map_machine.current.group)

    self.dialogue = Dialogue()
    self.dialogue_machine = Machine()


    self.dialogue_test_state = DialogueState("This is just an example text to use with gradual typing.")
    self.dialogue_test_state.create_node("Hello", "root")
    self.dialogue_test_state.create_node("Go to town", "1-1", "root")
    self.dialogue_test_state.create_node("Go to house", "1-2", "root")

    self.dialogue_test_state1 = DialogueState("This is just an another example to use with gradual typing.")
    self.dialogue_test_state1.create_node("Hello", "root")
    self.dialogue_test_state1.create_node("Go to town", "1-1", "root")
    self.dialogue_test_state1.create_node("Go to house", "1-2", "root")
    self.dialogue_engine : DialogueDisplayEngine = DialogueDisplayEngine(self.engine)



  #we need a function to make a new tile map to swap all the values


  # What is done on each frame when drawn
  def on_draw(self):
    #DRAWING CAMERA VIEW
    #this draw the camera surface based on the focus on the position of player
    view = -self.camera_view.viewpointPosition() + self.player.pos
    self.map_machine.current.on_draw(self.engine.surface, view)

    #draws the ui onto the camera surface so it doesn't get effected by the offset
    self.ui.on_draw(self.engine.surface)
    pg.draw.circle(self.engine.surface, "white", (int(self.player.pos.x), int(self.player.pos.y)), 5)

    if self.dialogue_machine.current:
      self.dialogue.draw(self.engine.surface)

    self.dialogue_engine.draw()


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
        self.dialogue_engine.dialogue_machine.add_dialogue(self.dialogue_test_state)
        self.dialogue_engine.dialogue_machine.add_dialogue(self.dialogue_test_state1)

      elif event.key == pg.K_ESCAPE:
        self.dialogue_engine.set_current(None)

  # Updates relevant game state information
  def on_update(self, delta):
    self.dt = delta

    #checks if there's a new update for next state
    self.map_machine.current.on_update(delta)

    #checks if sprite.feet is colliding with wall tiles
    for sprite in self.map_machine.current.group.sprites():
      try:
        if sprite.feet.collidelist(self.map_machine.current.walls) > -1:
            sprite.move_back(delta)

        if sprite.feet.collidelist(self.map_machine.current.interactable) > -1:
            self.dialogue_engine.dialogue_machine.add_dialogue(self.dialogue_test_state)
      except:
        pass

    self.ui.on_update()
    if self.dialogue_machine.current:
      self.dialogue.update(delta)

    self.dialogue_engine.update(delta=delta)