import pygame as pg
from random import randrange
from pygame.math import Vector2
from modules.state_machine import State
from components.player import Player
from components.enemy import Enemy
from components.ui import Interface

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

#this is the camera class handles the position of surface we see on the world surface
class Camera:
    def __init__(self, focus):
        #focus/lock on player
        self.focus : Player = focus
        self.view : pg.Surface = pg.display.set_mode((800, 600))
        self.origin = Vector2(800 // 2, 600 //2)
        self.viewP = self.origin.copy()


    def viewpoint(self) -> pg.Surface:
        pass

    def viewpointPosition(self):
        # Calculate the difference between the player and the center of the screen
        heading = self.focus.pos - self.origin
        # Move the camera gradually towards the player
        self.origin += heading * 0.05
        return -self.origin + Vector2(800 // 2, 600 // 2)


class GameState(State):
  def __init__(self, engine):
    super().__init__(engine)
    self.dt = 0                              # Initializes delta time
    self.clock = pg.time.Clock()             # Needed clock thing?
    font = pg.font.SysFont('comicsans', 15)  # Initializes font
    all_sprites = pg.sprite.Group()          # Makes all_sprites group for keeping all entities together to load

    # Makes camera and player at 400, 300. Adds player to all_sprites
    self.camera = Vector2(400, 300)
    self.player = Player((400, 300), all_sprites)
    self.ui = Interface(self.player)

    self.camera_view = Camera(self.player)

    #preset the world size to 4000, 4000 pixels
    self.world_surface = pg.Surface((4000, 4000))

    # Spawns 200 fly enemies at random locations
    self.flies = []
    for _ in range(250):
      self.flies.append(Enemy(self.player, (randrange(-3000, 3001), randrange(-3000, 3001)),"fly", 20, all_sprites))
    # Spawns 5 wasp enemies at random locations
    self.wasps = []
    for _ in range(50):
      self.wasps.append(Enemy(self.player, (randrange(-3000, 3001), randrange(-3000, 3001)),"wasp", 40, all_sprites))

  # What is done on each frame when drawn
  def on_draw(self):
    #clears the screen with blue color
    self.world_surface.fill((100, 170, 220))

    #DRAWING IN WORLD
    # Draws all fly enemies
    for fly in self.flies:
      #removes dead flies
      self.wasps = [wasp for wasp in self.wasps if wasp.health > 0]
      fly.on_draw(self.world_surface)
    # Draws all wasp enemies
    for wasp in self.wasps:
      #removes dead wasps
      self.flies = [fly for fly in self.flies if fly.health > 0]
      wasp.on_draw(self.world_surface)

    #draws the player particle effects
    self.player.player_particles.on_draw(self.world_surface)

    #draws player based in world location on surface
    self.world_surface.blit(self.player.image, self.player.rect.topleft)

    #DRAWING CAMERA VIEW
    #this draw the camera surface based on the focus on the position of player
    self.camera_view.view.blit(self.world_surface, self.camera_view.viewpointPosition())

    #draws the ui onto the camera surface so it doesn't get effected by the offset
    self.ui.on_draw(self.camera_view.view)

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
        for fly in self.flies:
          #checks if player collides with fly, hurts it
          if self.player.rect.colliderect(fly.rect):
            fly.hurt_enemy(5)
          #checks if player collides with fly, hurts it
        for wasp in self.wasps:
          if self.player.rect.colliderect(wasp.rect):
              wasp.hurt_enemy(5)
            
  # Updates relevant game state information
  def on_update(self, delta):
    self.dt = delta
    self.player.update()
    # Updates all fly enemies
    for fly in self.flies:
      fly.update(delta, self.world_surface)
    # Updates all wasp enemies
    for wasp in self.wasps:
      wasp.update(delta, self.world_surface)