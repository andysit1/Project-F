import pygame as pg
from pygame.math import Vector2
from settings import Settings
from modules.clock import Timer



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



    def debug_tongue(self):
        print("Position {}         Direction {}               Mode {}".format(self.tongue_driver.pos, self.tongue_driver.direction))

    def on_bendy_mode(self):
        self.on_switch_bendy_tongue_state()

    # iterate all points in list, when finish set the set to 0 (normal) -> gives back player controls back
    def traverse_bendy_tongue_path(self):

        #change in future..
        frame_skip = pg.math.lerp(4, 6, len(self.tongue_points) / 400)

        try:
            print(frame_skip)
            for i in range(0, int(frame_skip)):
                self.pos = self.tongue_points.pop(0)
            print("TRAVERSING", self.pos)
            self.rect.center = self.pos
        except:
            if len(self.tongue_points) <= 0: #finished traversal
                self.bendy_timer.stop()
                self.tongue_points.clear()


    #setter functions we should have..
    def set_player_pos(self, pos : pg.Vector2) -> None:
        self.pos = pos

    # Handles player actions based on key presses
    def handle_event(self, event, dt):

        self.player_movement(event, dt) # Moves the player

        #attacks
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_SPACE:
                self.attack_sweep.handle_attack_input(self.enemy_group)
            elif event.key == pg.K_c:

                self.tongue_driver.pos = self.pos.copy()
                self.tongue_driver.forward = self.vel
                self.tongue_driver.direction = 0

                self.bendy_timer.reset()
            elif event.key == pg.K_0:
                self.dialogue_machine.current = True
            elif event.key == pg.K_9:
                self.on_swap_map_state()
            elif event.key == pg.K_ESCAPE:
                self.dialogue_engine.set_current(None)


        if event.type == pg.KEYUP and event.key == pg.K_c:

            print("Normal Attack")
            self.tongue_driver.strength = 40
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

    def move_back(self, dt: float) -> None:
#         """
#         If called after an update, the sprite can move back
        # """
        self.pos = self._old_position
        self.rect.center = self.pos
        self.feet.midbottom = self.rect.midbottom

    #method to draw the players specific sprites that come with it through each states...
    #can be cosmetics, injuries, or other stuff
    def on_draw_player_sprites(self, surface, translate_functions):
        self.player_sprites.draw(surface=surface)

        if self.tongue_driver.pos:
            pg.draw.circle(surface, "RED", (self.tongue_driver.pos.x, self.tongue_driver.pos.y), 5.0)

        if len(self.tongue_points) > 0:
            screen_points = translate_functions(self.tongue_points)
            for points in screen_points:
                pg.draw.circle(surface, "RED", (points[0], points[1]), 10)


    def is_float_whole_numbers(self, val : float) -> bool:

        x = int(val)
        if x < 0:
            result = x - val
        else:
            result = x + val


        if 0.01 <= result <= 0.2:
            return True

        return False

    def tongue_point_appendable(self) -> None:
        if len(self.tongue_points) == 0:
            self.tongue_points.append(self.tongue_driver.pos.copy())
        else:
            last : pg.Vector2 = self.tongue_points[-1]
            if last.distance_to(self.tongue_driver.pos) > 0.5:
                self.tongue_points.append(self.tongue_driver.pos.copy())

    # Updates player positions based on velocity
    def update(self, dt):
        self._old_position = self.pos.copy()

        self.bendy_timer.update(dt)
        self.tongue_appending_timer.update(dt)


        self.player_sprites.update(dt)

        #handles when bendy_timer is active
        if self.bendy_timer.is_triggered():
            self.tongue_movement(dt=dt)
            self.tongue_driver.update(dt)
            self.tongue_point_appendable()

        elif len(self.tongue_points) > 0:
            self.traverse_bendy_tongue_path()
        else:


            #you multiple dt by 1 since you want to scale 1 second of time to be consistent
            #if we have a dash_timer active then we need to add the dash vel instead of the normal velocity of walking
            if self.dash_timer > 0:
                self.pos += self.dash_vel
                self.rect.center = self.pos
            else:
                if not self.bendy_timer.is_active:

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

            # Normalizes velocity vector in the diagonals (as cant normalize a vector of 0, which happens when not diagonal)
            try:

                self.vel = round(self.vel.normalize() * self.speed * dt, 3)
            except:
                pass

        #always running

        self.dash_timer -= 1 * dt #TODO change var name to not dash_timer but a general purpose timer

        #update the feet location based on the player mid bottom position
        self.feet.midbottom = self.rect.midbottom
