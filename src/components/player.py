import pygame as pg
from pygame.math import Vector2
from settings import Settings

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
        settings = Settings()
        #import, load, and convert image to Surface, then scale it to 70x70
        self.ui_pfp = settings.character_sprite['ui'].convert_alpha()
        self.up = settings.character_sprite['up'].convert_alpha()
        self.down = settings.character_sprite['down'].convert_alpha()
        self.right = settings.character_sprite['right'].convert_alpha()
        self.left = settings.character_sprite['left'].convert_alpha()
        self.image = self.down
        self.keypressed = []
        self.rect = self.image.get_rect(center=pos)
        self.pos = Vector2(pos)
        self.vel = Vector2(0, 0)
        self.speed = 100
        self.dash_timer : float = 0.0   #in seconds
        self.dash_time_length_seconds : float = 0.3 #in seconds
        self.dash_time_cooldown : float = 0.2
        self.dash_vel = Vector2(0, 0)
        self.max_health = 100
        self.direction = "down"

        #this health variable changes the ui
        self.health = 50

        #feet variable is used for wall collisions
        self.feet = pg.Rect(self.pos.x, self.pos.y, self.rect.width * 0.5, 8)
        self._old_position = None


    #setter functions we should have..
    def set_player_pos(self, pos : pg.Vector2) -> None:
        self.pos = pos

    # Handles player actions based on key presses
    def handle_event(self, event, dt):

        self.player_movement(event, dt) # Moves the player

        #dashing
        if event.type == pg.KEYDOWN and event.key == pg.K_z:
            #only add the timer when not active or below 0
            if self.dash_timer <= -self.dash_time_cooldown:
                self.dash_timer = self.dash_time_length_seconds
                self.dash_vel = self.vel * 2   #takes the current velocity at that given moment based on key input


    # Gets player movement vector based on key presses
    def player_movement(self, event, dt):
        # Checks for up, down, left, right arrow presses
        # Moves velocity + changes 'keypressed' that is used in updating character images
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_UP:
                self.vel.y = -self.speed * dt
                self.keypressed.append("up")
            elif event.key == pg.K_DOWN:
                self.vel.y = self.speed * dt
                self.keypressed.append("down")
            elif event.key == pg.K_RIGHT:
                self.vel.x = self.speed * dt
                self.keypressed.append("right")
            elif event.key == pg.K_LEFT:
                self.vel.x = -self.speed * dt
                self.keypressed.append("left")
        elif event.type == pg.KEYUP:
            if event.key == pg.K_UP:
                if self.vel.y < 0:
                    self.vel.y = 0
                try:
                    self.keypressed.remove("up")
                except:
                    pass
            elif event.key == pg.K_DOWN:
                if self.vel.y > 0:
                    self.vel.y = 0
                try:
                    self.keypressed.remove("down")
                except:
                    pass
            elif event.key == pg.K_RIGHT:
                if self.vel.x > 0:
                    self.vel.x = 0
                try:
                    self.keypressed.remove("right")
                except:
                    pass
            elif event.key == pg.K_LEFT:
                if self.vel.x < 0:
                    self.vel.x = 0
                try:
                    self.keypressed.remove("left")
                except:
                    pass
        # Normalizes velocity vector in the diagonals (as cant normalize a vector of 0, which happens when not diagonal)
        try:
            # Multiplies direction vector by speed, and time between frames, rounded to 3 decimal places
            self.vel = round(self.vel.normalize() * self.speed * dt, 3)
        except:
            pass

    def move_back(self, dt: float) -> None:
#         """
#         If called after an update, the sprite can move back
        # """
        self.pos = self._old_position
        self.rect.center = self.pos
        self.feet.midbottom = self.rect.midbottom

    # Updates player positions based on velocity
    def update(self, dt):
        self._old_position = self.pos.copy()

        #you multiple dt by 1 since you want to scale 1 second of time to be consistent
        self.dash_timer -= 1 * dt
        #if we have a dash_timer active then we need to add the dash vel instead of the normal velocity of walking
        if self.dash_timer > 0:
            self.pos += self.dash_vel
            self.rect.center = self.pos
        else:
            self.pos += self.vel
            self.rect.center = self.pos

        # Changes player image based on direction
        if (self.vel.length() > 0):
            self.direction = self.keypressed[0]
            if self.direction == "up":
                self.image = self.up
            elif self.direction == "down":
                self.image = self.down
            elif self.direction == "right":
                self.image = self.right
            elif self.direction == "left":
                self.image = self.left
        else:
            self.keypressed.clear()

        #update the feet location based on the player mid bottom position
        self.feet.midbottom = self.rect.midbottom
