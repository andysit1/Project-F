import pygame
from pygame import Vector2
import sys
import os
from pydantic import BaseModel
from modules.utils import load_settings, save_settings
from pyscroll.orthographic import BufferedRenderer
from pyscroll.data import PyscrollDataAdapter, TiledMapData
from pyscroll.group import PyscrollGroup
# Setup the environment by appending the current directory to the system path for asset access.


#Needs discussion about which settings we want to track...
class SettingsModel(BaseModel):
  def __init__(self):
     pass


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
    self.player_size = (70, 70)
    self.character_sprite = {
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

import pytmx
current_dir = os.path.dirname(os.path.dirname(__file__))
uitImagePath = os.path.join(current_dir,"[level tester]", "trial_blue", "blue_trial.tmx")
map_path = uitImagePath
#Caches the map into pygame surfaces...


class MapSettings():
  def __init__(self):
    self.layout = [1, 1, 1]
    self.surf = self.load_map(map_path)
    self.py_surf = pytmx.load_pygame(map_path)
    #represent where the player is in the self.layout
    self.pos : int = 0

  def update_visiblity(self):
    adj = [self.pos - 1, self.pos + 1]
    for pos in adj:
       if not pos < 0 or pos > len(adj):
          print(pos)

  def load_map(self, filename) -> pygame.Surface:
      tm = pytmx.load_pygame(filename)

      map_width = tm.width * tm.tilewidth
      map_height = tm.height * tm.tileheight
      map_surface = pygame.Surface((map_width, map_height))
      world_surface = pygame.Surface((map_width * len(self.layout), map_height))

      for layer in tm:
        print(layer)
        for x, y, gid in layer:
            tile = tm.get_tile_image_by_gid(gid)
            if tile:
                map_surface.blit(tile, (x * tm.tilewidth, y * tm.tileheight))

      #loads the world
      c = 0
      for layer in self.layout:
        world_surface.blit(map_surface, (c, 0))
        c += map_width
      return world_surface



def init_screen(width: int, height: int) -> pygame.Surface:
    screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
    return screen



class Player(pygame.sprite.Sprite):

    def __init__(self, pos, *groups):
        super().__init__(*groups)
        self.image = pygame.Surface((20, 20))
        self.image.fill(pygame.Color('dodgerblue1'))
        self.rect = self.image.get_rect(center=pos)
        self.pos = Vector2(pos)
        self.vel = Vector2(0, 0)
        self.speed = 4
        self.attack : bool = False
        self.origin = Vector2(1680 // 2, 1080 //2)

    def handle_event(self, event):
        #Handles player movement
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_d:
                self.vel.x = self.speed
            elif event.key == pygame.K_a:
                self.vel.x = -self.speed
            elif event.key == pygame.K_w:
                self.vel.y = -self.speed
            elif event.key == pygame.K_s:
                self.vel.y = self.speed
            elif event.key == pygame.K_SPACE:
                self.attack = True
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_d and self.vel.x > 0:
                self.vel.x = 0
            elif event.key == pygame.K_a and self.vel.x < 0:
                self.vel.x = 0
            elif event.key == pygame.K_w and self.vel.y < 0:
                self.vel.y = 0
            elif event.key == pygame.K_s and self.vel.y > 0:
                self.vel.y = 0

        try:
            self.vel = self.vel.normalize() * self.speed
        except:
            pass

    def get_attack_rect(self):
        return pygame.rect.Rect(
                self.pos.x,
                self.pos.y,
                self.image.get_width(),
                self.image.get_height()
              )


    def update(self):
    # Move the player.
      self.pos += self.vel
      self.rect.center = self.pos

    # Update player's rectangle position



class Camera(BufferedRenderer):
    def __init__(self, focus, data, size):
        super().__init__(data=data, size=size, clamp_camera=False, zoom=2)
                    #focus/lock on player
        self.focus : Player = focus
        self.view : pygame.Surface = pygame.display.set_mode((1680, 1080))
        self.origin = Vector2(1680 // 2 , 1080 //2)
        self.viewP = self.origin.copy()

    def viewpoint(self) -> pygame.Surface:
        pass

    def viewpointPosition(self):
        # Calculate the difference between the player and the center of the screen
        heading = self.focus.pos - self.origin
        # Move the camera gradually towards the player
        self.origin += heading * 0.05
        return -self.origin + self.focus.pos




if __name__ == "__main__":
    clock = pygame.time.Clock()

    pygame.init()
    pygame.font.init()
    screen = init_screen(1680, 1080)
    map_settings = MapSettings()
    all_sprites = pygame.sprite.Group()
    player = Player((400, 300), all_sprites)
    camera_player = Player((400, 300), all_sprites)

    camera = Camera(
       focus=player,
       data=TiledMapData(map_settings.py_surf),
       size=(1680, 1080)
    )

    camera.zoom = 2

    layout = [1, 1, 1]
    for position in layout:
       print(position)
    running = True

    screen_offset = Vector2(0,0)
    group = PyscrollGroup(map_layer=camera, default_layer=2)
    player.pos = camera.map_rect.center
    camera_player.pos = camera.map_rect.center
    group.add(player)
    group.add(camera_player)


    while running:
        player.update()
        camera_player.update()
        for event in pygame.event.get():
            player.handle_event(event=event)
            if event.type == pygame.QUIT:
                running = False

        view = camera.viewpointPosition() + player.pos
        #camera viewpoint doesnt align with the player position

        group.center(view)
        # camera._x_offset +=
        group.draw(screen)
        pygame.draw.circle(screen, (255, 255, 255), view, 10)



        # screen.fill("white")
        # camera_viewpoint = camera.viewpointPosition()
        # screen.blit(map_settings.surf, camera_viewpoint)
        # screen.blit(player.image, player.rect.topleft + camera_viewpoint)



        #creates an offset in the world to create damping effect

        pygame.display.flip()
        clock.tick(60)


    pygame.quit()