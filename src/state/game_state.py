import pygame as pg
from random import randrange
from pygame.math import Vector2
from modules.state_machine import State
from components.player import Player

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
    self.dt = 0                              # Initializes delta time
    self.clock = pg.time.Clock()             # Needed clock thing?
    font = pg.font.SysFont('comicsans', 15)  # Initializes font
    all_sprites = pg.sprite.Group()          # Makes all_sprites group for keeping all entities together to load
   
    # Makes camera and player at 400, 300. Adds player to all_sprites
    self.camera = Vector2(400, 300)
    self.player = Player((400, 300), all_sprites)

    # Spawns 500 test rectangles
    self.background_rects = [pg.Rect(randrange(-3000, 3001), randrange(-3000, 3001), 20, 20) for _ in range(500)]

  # What is done on each frame when drawn
  def on_draw(self, surface):
    surface.fill((30, 30, 30))

    # Camera movement
    heading = self.player.pos - self.camera
    self.camera += heading * 0.05
    offset = -self.camera + Vector2(400, 300)

    # Draws all background rectangles
    for background_rect in self.background_rects:
      topleft = background_rect.topleft + offset
      pg.draw.rect(surface, (200, 50, 70), (topleft, background_rect.size))

    # Draws player
    surface.blit(self.player.image, self.player.rect.topleft+offset)

    # Draws a yellow circle at the player's origin
    origin = self.player.rect.topleft+offset
    pg.draw.circle(surface, "yellow", origin, 5)

    # --- Junk test code for info on screen ---
    # velocity_text = font.render(f"Velocity: {self.player.vel.length()}", True, pg.Color('white'))
    # surface.blit(velocity_text, (20, 20))

  # Handles events (ie. key presses)
  def on_event(self, event):
    # Calls player's handle_event function (player's movements and attacks)
    self.player.handle_event(event=event, dt=self.dt)

  # Updates relevant game state information
  def on_update(self, delta):
    self.dt = delta
    self.player.update()