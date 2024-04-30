import pygame as pg
from random import randrange
from pygame.math import Vector2
from modules.state_machine import State, Machine
from components.player import Player
from components.enemy import Enemy, HealthBar
from components.ui import Interface
from components.camera import Camera
from settings import Settings, MapSettings
from components.particles import ParticleGenerator
from components.attack import AttackHandler


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
    all_sprites = pg.sprite.Group()          # Makes all_sprites group for keeping all entities together to load

    # Makes camera and player at 400, 300. Adds player to all_sprites
    self.camera = Vector2(400, 300)
    self.player = Player((400, 300), all_sprites)
    self.map_settings = MapSettings()        #init map settings
    self.map_machine = Machine()
    self.map_machine.current = self.map_settings.maps.get("base") #set the first state as base
    self.map_machine.current.group.add(self.player)


    self.ui = Interface(self.player)
    self.camera_view = Camera(self.player)
    self.particle_gen = ParticleGenerator()

    self.flies = []
    for _ in range(30):
      fly_obj = Enemy(self.player, (randrange(0, 1080), randrange(0, 1080)), self.settings.enemy_sprite['fly'].convert_alpha(), 20, all_sprites)
      health_bar_obj = HealthBar(fly_obj)
      self.flies.append(fly_obj)
      self.map_machine.current.group.add(fly_obj)
      self.map_machine.current.group.add(health_bar_obj)


    self.wasps = []
    for _ in range(30):
      wasp_obj = Enemy(self.player, (randrange(0, 1080), randrange(0, 1080)), self.settings.enemy_sprite['wasp'].convert_alpha(), 40, all_sprites)
      health_bar_obj = HealthBar(wasp_obj)

      self.wasps.append(wasp_obj)
      self.map_machine.current.group.add(wasp_obj)
      self.map_machine.current.group.add(health_bar_obj)
      
      
    self.last_attack_rect = None  # To store the last attack hitbox
    self.attack_handler = AttackHandler(self)

  # What is done on each frame when drawn
  def on_draw(self):

    #DRAWING CAMERA VIEW
    #this draw the camera surface based on the focus on the position of player
    view = -self.camera_view.viewpointPosition() + self.player.pos
    self.map_machine.current.on_draw(self.engine.surface, view)

    #draws the ui onto the camera surface so it doesn't get effected by the offset
    self.ui.on_draw(self.engine.surface)
    pg.draw.circle(self.engine.surface, "white", (int(self.player.pos.x), int(self.player.pos.y)), 5)
    # --- Junk test code for info on screen ---
    # velocity_text = font.render(f"Velocity: {self.player.vel.length()}", True, pg.Color('white'))
    # surface.blit(velocity_text, (20, 20))

  # Handles events (ie. key presses)
  def on_event(self, event):
    # Calls player's handle_event function (player's movements and attacks)
    self.player.handle_event(event=event, dt=self.dt)
    # If space is pressed, player attacks enemies
    if event.type == pg.KEYDOWN:
      if event.key == pg.K_SPACE:
        # for fly in self.flies:
        #   #checks if player collides with fly, hurts it
        #   if self.player.rect.colliderect(fly.rect):
        #     fly.hurt_enemy(5)
        #     # particle_obj = self.particle_gen.generate_blood_particles(fly)
        #     # self.map_machine.current.group.add(particle_obj)

        #   #checks if player collides with fly, hurts it
        # for wasp in self.wasps:
        #   if self.player.rect.colliderect(wasp.rect):
        #       wasp.hurt_enemy(5)
        self.attack_handler.perform_attack()


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
      except:
        pass
    self.ui.on_update()
