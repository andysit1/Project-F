import pygame as pg
from pygame.math import Vector2
from settings import Settings
from modules.clock import Timer
from modules.state_machine import Machine
from typing import Callable

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

# Taken from https://github.com/clear-code-projects/pygame-gta2/blob/master/gta2_pygame.py
class Driver:
    def __init__(self):
        self.angle = 0
        self.rotation_speed = 1.3
        self.direction = 0
        self.forward = pg.math.Vector2(0,-1)
        self.active = True #always increasing speeds...
        self.pos : pg.math.Vector2 = None
        self.strength : int = 40



    def get_rotation(self):
        #direction is always
        self.forward.rotate_ip(self.rotation_speed * self.direction)

    def accelerate(self, dt):
        self.strength += 0.2
        if self.active:
            self.pos += self.forward * self.strength * dt

    def update(self, dt):
        self.get_rotation()
        self.accelerate(dt)


class Player(pg.sprite.Sprite):
    def __init__(self, pos, *groups):
        super().__init__(groups)
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


        #TONGUE VARS
        self.tongue_turn_strength : int = 5
        self.tongue_points = []
        self.tongue_driver : Driver = Driver()
        self.tongue_driver.pos = None
        self.bendy_timer = Timer(0.4)
        self.tongue_appending_timer = Timer(0.3)
        self.tongue_appending_timer.is_active = True
        self.tongue_travel_speeds = 10

        from components.attack import AttackSprite
        from components.attack import SweepAttackSprite

        self.player_sprites : pg.sprite.Group = pg.sprite.Group()
        self.attack_sprite_test = AttackSprite(self, self.player_sprites)
        self.attack_sweep = SweepAttackSprite(self, self.player_sprites)




    #should handle interaction of the tongue ie walls, enemies, and etc.
    def handle_tongue_collsion(self):
        # if self.tongue_driver[-1] collides with x group ... then
        #     do x activity
        pass

    def is_tongue_out(self) -> bool:
        if len(self.tongue_points) > 0:
            return True
        return False


    def traverse_bendy_tongue_path(self, is_grapple:bool=False):
        #TODO/BUG optimize this function later, this is really bad code

        frame_skip = pg.math.lerp(2, 6, len(self.tongue_points) / 400) #on frame change decide how many frames to make gone
        try:
            for i in range(0, int(frame_skip)):
                if is_grapple:
                    self.pos = self.tongue_points.pop(0)
                    self.rect.center = self.pos
                else:
                    self.tongue_points.pop()
        except:
            if len(self.tongue_points) <= 0: #finished traversal
                self.bendy_timer.stop()
                self.tongue_points.clear()

    def set_player_pos(self, pos : pg.Vector2) -> None:
        self.pos = pos

    def init_tongue_position_direction_timer(self):
        self.tongue_driver.pos = self.pos.copy()
        self.tongue_driver.forward = self.vel #TODO/BUG make this self.vel 1 or 0.. causes issue moving
        self.tongue_driver.direction = 0
        self.bendy_timer.reset()

    def handle_event(self, event, dt):
        self.player_movement(event, dt)

        if event.type == pg.KEYDOWN:
            if event.key == pg.K_c:
                self.init_tongue_position_direction_timer()

        if event.type == pg.KEYUP and event.key == pg.K_c:
            self.tongue_driver.strength = 40 #TODO/BUG make into constant settings variable
            self.bendy_timer.stop()

        #dashing
        if event.type == pg.KEYDOWN and event.key == pg.K_z:
            #only add the timer when not active or below 0
            if self.dash_timer <= -self.dash_time_cooldown:
                self.dash_timer = self.dash_time_length_seconds
                self.dash_vel = self.vel * 2   #takes the current velocity at that given moment based on key input

    def tongue_movement(self, dt):
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT]:
            self.tongue_driver.direction += -self.tongue_turn_strength * dt
        if keys[pg.K_RIGHT]:
            self.tongue_driver.direction += self.tongue_turn_strength * dt

        self.tongue_driver.direction = pg.math.clamp(self.tongue_driver.direction, -1, 1)


    # Gets player movement vector based on key presses
    def player_movement(self, event, dt):
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

    #TODO fix player movement in game (sticking to walls)
    def move_back(self, dt: float) -> None:
        self.pos = self._old_position
        self.rect.center = self.pos
        self.feet.midbottom = self.rect.midbottom

    #method to draw the players specific sprites that come with it through each states...
    #can be cosmetics, injuries, or other stuff in future
    def on_draw_player_sprites(self, surface : pg.Surface, translate_functions : Callable = None):
        self.player_sprites.draw(surface=surface)

        if self.tongue_driver.pos:
            pg.draw.circle(surface, "RED", (self.tongue_driver.pos.x, self.tongue_driver.pos.y), 5.0)

        if self.is_tongue_out():
            if translate_functions:
                screen_points = translate_functions(self.tongue_points)
            else:
                screen_points = self.tongue_points

            for points in screen_points:
                pg.draw.circle(surface, "RED", (points[0], points[1]), 10)


    def tongue_point_appendable(self) -> None:
        if len(self.tongue_points) == 0:
            self.tongue_points.append(self.tongue_driver.pos.copy())
        else:
            #checks tongue distance from last point if its large enough of a gap to append for consistence spacing as we increase velocity
            last : pg.Vector2 = self.tongue_points[-1]
            if last.distance_to(self.tongue_driver.pos) > 0.5:
                self.tongue_points.append(self.tongue_driver.pos.copy())

    # Updates player positions based on velocity
    def update(self, dt):
        self._old_position = self.pos.copy()

        self.bendy_timer.update(dt)
        self.tongue_appending_timer.update(dt)

        self.player_sprites.update(dt)

        """
            LOGIC FLOW
            1.) when driver is active (tongue is moving)
            2.) when driver is not active but we have points still existing (tongue is still out of mouth)
            3.) when tongue is not moving and tongue is not out, we can just run around
        """

        if self.bendy_timer.is_triggered():
            self.tongue_movement(dt=dt)
            self.tongue_driver.update(dt)
            self.tongue_point_appendable()
        elif self.is_tongue_out():
            self.traverse_bendy_tongue_path()
        else:

            if self.dash_timer > 0:
                self.pos += self.dash_vel
                self.rect.center = self.pos
            else:
                if not self.bendy_timer.is_active:

                    self.pos += self.vel
                    self.rect.center = self.pos

            # Changes player image based on direction
            if (self.vel.length() > 0):
                try:
                    self.direction = self.keypressed[0]  #TODO/BUG Path Traversal causes issues since we have vel > 0 and no keys pressed.. this is quick fix but not the best...
                    if self.direction == "up":
                        self.image = self.up
                    elif self.direction == "down":
                        self.image = self.down
                    elif self.direction == "right":
                        self.image = self.right
                    elif self.direction == "left":
                        self.image = self.left
                except:
                    pass
            else:
                self.keypressed.clear()

            # Normalizes velocity vector in the diagonals (as cant normalize a vector of 0, which happens when not diagonal)
            try:
                self.vel = round(self.vel.normalize() * self.speed * dt, 3)
            except:
                pass

        self.dash_timer -= 1 * dt
        self.feet.midbottom = self.rect.midbottom
