import pygame as pg
from pygame.math import Vector2
from components.particles import Particles

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
        #import, load, and convert image to Surface, then scale it to 70x70
        self.up = pg.transform.scale(pg.image.load("./assets/player_assets/up.png").convert_alpha() , (70, 70))
        self.down = pg.transform.scale(pg.image.load("./assets/player_assets/down.png").convert_alpha() , (70, 70))
        self.right = pg.transform.scale(pg.image.load("./assets/player_assets/right.png").convert_alpha() , (70, 70))
        self.left = pg.transform.scale(pg.image.load("./assets/player_assets/left.png").convert_alpha() , (70, 70))
        self.image = self.down
        self.keypressed = []
        self.rect = self.image.get_rect(center=pos)
        self.pos = Vector2(pos)
        self.vel = Vector2(0, 0)
        self.speed = 400
        self.dash_timer : float = 0.0
        self.dash_vel = Vector2(0, 0)
        self.player_particles = Particles(self) #init the particles system for player

    # Handles player actions based on key presses
    def handle_event(self, event, dt):

        self.player_movement(event, dt) # Moves the player
        #WIP -- for attack --
        #if event.type == pg.KEYDOWN and event.key == pg.K_SPACE:
            # print("space")

        #dashing
        if event.type == pg.KEYDOWN and event.key == pg.K_z:
            #only add the timer when not active or below 0
            if self.dash_timer <= 0:
                self.player_particles.generate_particles_frog_dash() #generates the particles
                self.dash_timer = 3
                self.dash_vel = self.vel * 2   #takes the current velocity at that given moment based on key input


    # Gets player movement vector based on key presses
    def player_movement(self, event, dt):
        # Checks for up, down, left, right arrow presses
        # Moves velocity + changes 'keypressed' that is used in updating character images
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_UP:
                self.vel.y = -self.speed * dt
                self.keypressed.append(self.up)
            elif event.key == pg.K_DOWN:
                self.vel.y = self.speed * dt
                self.keypressed.append(self.down)
            elif event.key == pg.K_RIGHT:
                self.vel.x = self.speed * dt
                self.keypressed.append(self.right)
            elif event.key == pg.K_LEFT:
                self.vel.x = -self.speed * dt
                self.keypressed.append(self.left)
        elif event.type == pg.KEYUP:
            if event.key == pg.K_UP and self.vel.y < 0:
                self.vel.y = 0
                self.keypressed.remove(self.up)
            elif event.key == pg.K_DOWN and self.vel.y > 0:
                self.vel.y = 0
                self.keypressed.remove(self.down)
            elif event.key == pg.K_RIGHT and self.vel.x > 0:
                self.vel.x = 0
                self.keypressed.remove(self.right)
            elif event.key == pg.K_LEFT and self.vel.x < 0:
                self.vel.x = 0
                self.keypressed.remove(self.left)

        # Normalizes velocity vector in the diagonals (as cant normalize a vector of 0, which happens when not diagonal)
        try:
            # Multiplies direction vector by speed, and time between frames, rounded to 3 decimal places
            self.vel = round(self.vel.normalize() * self.speed * dt, 3)
        except:
            pass

    # Updates player positions based on velocity
    def update(self):
        #if we have a dash_timer active then we need to add the dash vel instead of the normal velocity of walking
        if self.dash_timer > 0:
            self.dash_timer -= 0.2
            self.pos += self.dash_vel
            self.rect.center = self.pos
        else:
            self.pos += self.vel
            self.rect.center = self.pos

        # Changes player image based on direction
        if (self.vel.length() > 0):
            self.image = self.keypressed[0]
        else:
            self.keypressed.clear()