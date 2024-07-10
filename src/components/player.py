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
        self.load_images(settings)
        self.image = self.down
        self.keypressed = []
        self.rect = self.image.get_rect(center=pos)
        self.pos = Vector2(pos)
        self.vel = Vector2(0, 0)
        self.speed = 100
        self.dash_timer = 0.0  # in seconds
        self.dash_time_length_seconds = 0.3  # in seconds
        self.dash_time_cooldown = 0.2
        self.dash_vel = Vector2(0, 0)
        self.max_health = 100
        self.direction = "down"
        self.health = 50
        self.feet = pg.Rect(self.pos.x, self.pos.y, self.rect.width * 0.5, 8)
        self._old_position = None

    def load_images(self, settings):
        self.ui_pfp = settings.character_sprite['ui'].convert_alpha()
        self.up = settings.character_sprite['up'].convert_alpha()
        self.down = settings.character_sprite['down'].convert_alpha()
        self.right = settings.character_sprite['right'].convert_alpha()
        self.left = settings.character_sprite['left'].convert_alpha()

    def handle_event(self, event, dt):
        self.player_movement(event, dt)
        if event.type == pg.KEYDOWN and event.key == pg.K_z:
            self.start_dash()

    def start_dash(self):
        if self.dash_timer <= -self.dash_time_cooldown:
            self.dash_timer = self.dash_time_length_seconds
            self.dash_vel = self.vel * 2

    def player_movement(self, event, dt):
        if event.type == pg.KEYDOWN:
            self.handle_keydown(event, dt)
        elif event.type == pg.KEYUP:
            self.handle_keyup(event)

        self.normalize_velocity(dt)

    def handle_keydown(self, event, dt):
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

    def handle_keyup(self, event):
        if event.key == pg.K_UP:
            self.stop_movement("up", self.vel.y < 0)
        elif event.key == pg.K_DOWN:
            self.stop_movement("down", self.vel.y > 0)
        elif event.key == pg.K_RIGHT:
            self.stop_movement("right", self.vel.x > 0)
        elif event.key == pg.K_LEFT:
            self.stop_movement("left", self.vel.x < 0)

    def stop_movement(self, direction, condition):
        if condition:
            if direction in ["up", "down"]:
                self.vel.y = 0
            else:
                self.vel.x = 0
        try:
            self.keypressed.remove(direction)
        except ValueError:
            pass

    def normalize_velocity(self, dt):
        try:
            self.vel = round(self.vel.normalize() * self.speed * dt, 3)
        except ValueError:
            pass

    def move_back(self, dt: float) -> None:
        self.pos = self._old_position
        self.rect.center = self.pos
        self.feet.midbottom = self.rect.midbottom

    def update(self, dt):
        self._old_position = self.pos.copy()
        self.update_dash_timer(dt)
        self.update_position()
        self.update_image()
        self.update_feet_position()

    def update_dash_timer(self, dt):
        self.dash_timer -= 1 * dt

    def update_position(self):
        if self.dash_timer > 0:
            self.pos += self.dash_vel
        else:
            self.pos += self.vel
        self.rect.center = self.pos

    def update_image(self):
        if self.vel.length() > 0:
            self.direction = self.keypressed[0]
            self.change_image_based_on_direction()
        else:
            self.keypressed.clear()

    def change_image_based_on_direction(self):
        if self.direction == "up":
            self.image = self.up
        elif self.direction == "down":
            self.image = self.down
        elif self.direction == "right":
            self.image = self.right
        elif self.direction == "left":
            self.image = self.left

    def update_feet_position(self):
        self.feet.midbottom = self.rect.midbottom
