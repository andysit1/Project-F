import pygame as pg
from random import randrange
from pygame.math import Vector2
from modules.state_machine import State
import time
import math

class Player(pg.sprite.Sprite):

    def __init__(self, pos, *groups):
        super().__init__(*groups)
        self.image = pg.Surface((30, 30))
        self.image.fill(pg.Color('dodgerblue1'))
        self.rect = self.image.get_rect(center=pos)
        self.pos = Vector2(pos)
        self.vel = Vector2(0, 0)
        self.speed = 4

    def handle_event(self, event, dt):
        #Handles player movement
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_d:
                self.vel.x = self.speed * dt
            elif event.key == pg.K_a:
                self.vel.x = -self.speed * dt
            elif event.key == pg.K_w:
                self.vel.y = -self.speed * dt
            elif event.key == pg.K_s:
                self.vel.y = self.speed * dt
        elif event.type == pg.KEYUP:
            if event.key == pg.K_d and self.vel.x > 0:
                self.vel.x = 0
            elif event.key == pg.K_a and self.vel.x < 0:
                self.vel.x = 0
            elif event.key == pg.K_w and self.vel.y < 0:
                self.vel.y = 0
            elif event.key == pg.K_s and self.vel.y > 0:
                self.vel.y = 0

        # Normalizes the velocity of the diagonal movement vector
        if self.vel.x != 0 and self.vel.y != 0:
            self.vel = self.vel.normalize() * self.speed

    def update(self):
        # Move the player.
      self.pos += self.vel
      self.rect.center = self.pos

class GameState(State):
  def __init__(self, engine):
    super().__init__(engine)

    self.clock = pg.time.Clock()
    all_sprites = pg.sprite.Group()
    self.camera = Vector2(400, 300)
    self.player = Player((400, 300), all_sprites)

    self.background_rects = [pg.Rect(randrange(-3000, 3001), randrange(-3000, 3001), 20, 20)
                        for _ in range(500)]
    self.dt = 0
    self.current_attack = 0
    #camera variables


  def on_draw(self, surface):
    surface.fill((30, 30, 30))

    heading = self.player.pos - self.camera
    self.camera += heading * 0.05
    offset = -self.camera + Vector2(400, 300)

    for background_rect in self.background_rects:
            topleft = background_rect.topleft + offset
            pg.draw.rect(surface, (200, 50, 70), (topleft, background_rect.size))

    surface.blit(self.player.image, self.player.rect.topleft+offset)

    origin = self.player.rect.topleft+offset
    pg.draw.circle(surface, "yellow", origin, 5)

    if self.current_attack > 0:
        attack_rect = pg.rect.Rect(origin[0] + self.player.rect.width, origin[1],self.player.rect.width * 2, self.player.rect.height)
        pg.draw.rect(surface, "red", attack_rect)

        rect = pg.Rect(origin[0] - 36, origin[1] - 50, 100, 100)  # Rectangle to contain the arc
        pg.draw.arc(surface, "red", rect, 0, 3.14, 5)  # Draw half circle (0 to pi radians)

        self.current_attack -= 0.2

    # origin = self.player.pos
    # attack_rect = pg.Rect()

    # Displays character velocity for testing
    font = pg.font.SysFont('comicsans', 15)
    velocity_text = font.render(f"Velocity: {self.player.vel.length()}", True, pg.Color('white'))
    surface.blit(velocity_text, (20, 20))

  def on_event(self, event):
    self.player.handle_event(event=event, dt=self.dt)
    if event.type == pg.KEYUP and event.key == pg.K_SPACE:
        self.current_attack = 2



  def on_update(self, delta):
    self.dt = delta
    self.player.update()
