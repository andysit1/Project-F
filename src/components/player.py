import pygame as pg
from pygame.math import Vector2

'''
  --- Player class ---
  This class is responsible for controlling everything about the player.
  (ie. player movement, player attacks, player health...)

  Functions:
    __init__ : Initializes the player object
    handle_event : Handles player events (ie. key presses)
    player_movement : Handles player directional movement
    update : Updates player information each frame/update
'''

class Player(pg.sprite.Sprite):
    def __init__(self, pos, *groups):
        super().__init__(*groups)
        self.image = pg.Surface((30, 30))
        self.image.fill(pg.Color('green'))
        self.rect = self.image.get_rect(center=pos)
        self.pos = Vector2(pos)
        self.vel = Vector2(0, 0)
        self.speed = 400

    # Handles player actions based on key presses
    def handle_event(self, event, dt):
        # Moves the player
        self.player_movement(event, dt)
        
        # Will be for attacking --WIP--
        if event.type == pg.KEYDOWN and event.key == pg.K_SPACE:
            print('space')


    # Gets player movement vector based on key presses
    def player_movement(self, event, dt):
        # Checks for up, down, left, right arrow presses
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_UP:
                self.vel.y = -self.speed * dt
            elif event.key == pg.K_DOWN:
                self.vel.y = self.speed * dt
            elif event.key == pg.K_RIGHT:
                self.vel.x = self.speed * dt
            elif event.key == pg.K_LEFT:
                self.vel.x = -self.speed * dt
        elif event.type == pg.KEYUP:
            if event.key == pg.K_UP and self.vel.y < 0:
                self.vel.y = 0
            elif event.key == pg.K_DOWN and self.vel.y > 0:
                self.vel.y = 0
            elif event.key == pg.K_RIGHT and self.vel.x > 0:
                self.vel.x = 0
            elif event.key == pg.K_LEFT and self.vel.x < 0:
                self.vel.x = 0

        # Normalizes velocity vector in the diagonals (as cant normalize a vector of 0, which happens when not diagonal)
        try:
            # Multiplies direction vector by speed, and time between frames, rounded to 3 decimal places
            self.vel = round(self.vel.normalize() * self.speed * dt, 3)
        except:
            pass
      
    # Updates player positions based on velocity
    def update(self):
        self.pos += self.vel
        self.rect.center = self.pos