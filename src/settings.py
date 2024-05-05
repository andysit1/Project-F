import pygame
from pygame import Vector2
import sys
import os
from pyscroll.data import TiledMapData
from modules.state_machine import State

# Setup the environment by appending the current directory to the system path for asset access.

#Const Variables ...
SCREEN = (1600, 1000)
import pytmx
from pyscroll.orthographic import BufferedRenderer
from pyscroll.group import PyscrollGroup
from settings import SCREEN

current_dir = os.path.dirname(os.path.dirname(__file__))
uitImagePath = os.path.join(current_dir,"[level tester]", "trial_blue", "unbound_blue.tmx")
map_path = uitImagePath


class MapState(State):
    def __init__(self, data, walls):
        self.map_layer : BufferedRenderer = BufferedRenderer(
            data = data,
            size=(SCREEN[0], SCREEN[1])
        )
        self.map_layer.zoom = 2.5
        self.group : PyscrollGroup = PyscrollGroup(map_layer=self.map_layer, default_layer=2)

        self.walls = walls

    def on_draw(self, surface, center):
        self.group.center(value=center)
        self.group.draw(surface=surface)

    def on_update(self, delta):
        self.group.update(delta)

class Settings():
  """
    A class to manage and provide settings and assets for the game, such as player ships, backgrounds, level-up screens, game over screens, and projectiles.

  """
  def __init__(self):
    current_dir = os.path.dirname(os.path.dirname(__file__))
    sys.path.append(current_dir)

    """
    Initializes the Settings class by loading all necessary game assets from the assets directory and creating theme sets.
    """
    # Paths for various game assets are constructed here using `os.path.join`
    self.frog_right  = os.path.join(current_dir, "assets", "player_assets", "right.png")
    self.frog_left  = os.path.join(current_dir, "assets", "player_assets", "left.png")
    self.frog_up  = os.path.join(current_dir, "assets", "player_assets", "up.png")
    self.frog_down  = os.path.join(current_dir, "assets", "player_assets", "down.png")

    self.src = current_dir


    #dict representing frog sprites
    self.player_size = (20, 20)
    self.ui_player_size = (70, 70)
    self.character_sprite = {
      'ui' : pygame.transform.scale(pygame.image.load(self.frog_right), self.ui_player_size),
      'right' :  pygame.transform.scale(pygame.image.load(self.frog_right), self.player_size),
      'left' :  pygame.transform.scale(pygame.image.load(self.frog_left), self.player_size),
      'up' :  pygame.transform.scale(pygame.image.load(self.frog_up), self.player_size),
      'down' :  pygame.transform.scale(pygame.image.load(self.frog_down), self.player_size)
    }

    #dict representing enemy sprites
    self.enemy_size = (40, 40)
    self.enemy_sprite = {
      'fly' : pygame.transform.scale(pygame.image.load("{}/assets/".format(self.src) + 'fly' + ".png"), self.enemy_size),
      'wasp' : pygame.transform.scale(pygame.image.load("{}/assets/".format(self.src) + 'wasp' + ".png"), self.enemy_size),
    }

#Caches the map into pygame surfaces...


class MapSettings():
    def __init__(self):
        self.layout = [1, 1, 1]
        self.py_surf = pytmx.load_pygame(map_path)
        #represent where the player is in the self.layout
        self.pos : int = 0
        self.walls = []
        self.maps = {}

        self.load_map("base", map_path)

    def load_all_maps(self):
        #this will loop through a file in the future and load all maps...
        #for now we can ignore
        return NotImplemented

    def load_map(self, name, filename) -> None:
        surf = pytmx.load_pygame(filename)
        walls = []

        for layer in surf:
            if layer.name == "wall_collision":
                for obj in layer:
                    if obj[2] != 0:
                        walls.append(pygame.Rect(obj[0] * 16, obj[1] * 16, 16, 16))

        self.walls = walls

        self.maps = {
            name : MapState(TiledMapData(surf), walls)
        }


def init_screen(width: int, height: int) -> pygame.Surface:
    screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
    return screen


# class Player(pygame.sprite.Sprite):

#     def __init__(self, pos, *groups):
#         super().__init__(*groups)
#         self.image = pygame.Surface((10, 10))
#         self.image.fill(pygame.Color('dodgerblue1'))
#         self.rect = self.image.get_rect(center=pos)
#         self.pos = Vector2(pos)
#         self.vel = Vector2(0, 0)
#         self.speed = 5
#         self.attack : bool = False
#         self.origin = Vector2(1680 // 2, 1080 //2)

#         self._old_position = None
#         self.feet = pygame.Rect(self.pos.x, self.pos.y, self.rect.width * 0.5, 8)

#     def handle_event(self, event, dt):
#         #Handles player movement
#         if event.type == pygame.KEYDOWN:
#             if event.key == pygame.K_d:
#                 self.vel.x = self.speed * dt
#             elif event.key == pygame.K_a:
#                 self.vel.x = -self.speed * dt
#             elif event.key == pygame.K_w:
#                 self.vel.y = -self.speed * dt
#             elif event.key == pygame.K_s:
#                 self.vel.y = self.speed * dt
#             elif event.key == pygame.K_SPACE:
#                 self.attack = True

#         try:
#             self.vel = self.vel.normalize() * self.speed
#         except:
#             pass

#     def get_attack_rect(self):
#         return pygame.rect.Rect(
#                 self.pos.x,
#                 self.pos.y,
#                 self.image.get_width(),
#                 self.image.get_height()
#               )
#     # Update player's rectangle position
#     def move_back(self, dt: float) -> None:
#         """
#         If called after an update, the sprite can move back

#         """
#         self.pos = self._old_position
#         self.rect.center = self.pos
#         self.feet.midbottom = self.rect.midbottom

#     def update(self, dt):
#     # Move the player.
#         self._old_position = self.pos[:]
#         self.pos += self.vel
#         self.rect.center = self.pos
#         self.feet.midbottom = self.rect.midbottom


# class Camera(BufferedRenderer):
#     def __init__(self, focus, data, size):
#         super().__init__(data=data, size=size, clamp_camera=True, zoom=2.5)
#                     #focus/lock on player
#         self.focus : Player = focus
#         self.view : pygame.Surface = pygame.display.set_mode((1680, 1080))
#         self.origin = Vector2(1680 // 2 , 1080 //2)
#         self.viewP = self.origin.copy()

#     def viewpoint(self) -> pygame.Surface:
#         pass

#     def viewpointPosition(self):
#         # Calculate the difference between the player and the center of the screen
#         heading = self.focus.pos - self.origin
#         # Move the camera gradually towards the player
#         self.origin += heading * 0.05
#         return -self.origin + self.focus.pos


# if __name__ == "__main__":
#     clock = pygame.time.Clock()

#     pygame.init()
#     pygame.font.init()
#     screen = init_screen(SCREEN[0], SCREEN[1])
#     map_settings = MapSettings()
#     all_sprites = pygame.sprite.Group()
#     player = Player((400, 300), all_sprites)

#     camera = Camera(
#        focus=player,
#        data=TiledMapData(map_settings.py_surf),
#        size=(1680, 1080)
#     )

#     running = True
#     player.pos = (176, 319.5)

#     map_machine = Machine()
#     map_machine.current = map_settings.maps.get('base')
#     map_machine.current.group.add(player)

#     import time
#     previous_time = time.time()

#     while running:
#         dt = time.time() - previous_time
#         previous_time = time.time()

#         for event in pygame.event.get():
#             player.handle_event(event=event, dt=dt)
#             if event.type == pygame.QUIT:
#                 running = False

#         map_machine.current.on_update(dt)
#         for sprite in map_machine.current.group.sprites():
#             if sprite.feet.collidelist(map_settings.walls) > -1:
#                 sprite.move_back(dt)

#         view = -camera.viewpointPosition() + player.pos
#         #camera viewpoint doesnt align with the player position

#         # camera._x_offset +=
#         map_machine.current.on_draw(screen, view)

#         pygame.draw.circle(screen, (255, 255, 255), (0, 0), 10)
#         pygame.display.flip()
#         clock.tick(60)
#     pygame.quit()
