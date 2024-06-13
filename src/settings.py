import pygame
import sys
import os
from pyscroll.data import TiledMapData
from modules.state_machine import State

# Setup the environment by appending the current directory to the system path for asset access.

#Const Variablee ...
SCREEN = (1600, 1000)
import pytmx
from pyscroll.orthographic import BufferedRenderer
from pyscroll.group import PyscrollGroup
from settings import SCREEN
from random import randint

current_dir = os.path.dirname(os.path.dirname(__file__))
uitImagePath = os.path.join(current_dir,"[level tester]", "trial_blue", "unbound_blue.tmx")
map_path = uitImagePath



#this should be moved else where
class MapState(State):
    def __init__(self, data, walls, interactable, player, enemy_grp):

        self.map_layer : BufferedRenderer = BufferedRenderer(
            data = data,
            size=(SCREEN[0], SCREEN[1])
        )
        self.map_layer.zoom = 5
        self.group : PyscrollGroup = PyscrollGroup(map_layer=self.map_layer, default_layer=2)

        self.player = player
        self.enemy_grp = enemy_grp
        self.walls = walls
        self.interactable = interactable


        self.group.add(self.player)
        self.group.add(self.enemy_grp)

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
    self.player_size = (16, 16)
    self.ui_player_size = (70, 70)
    self.character_sprite = {
      'ui' : pygame.transform.scale(pygame.image.load(self.frog_right), self.ui_player_size),
      'right' :  pygame.transform.scale(pygame.image.load(self.frog_right), self.player_size),
      'left' :  pygame.transform.scale(pygame.image.load(self.frog_left), self.player_size),
      'up' :  pygame.transform.scale(pygame.image.load(self.frog_up), self.player_size),
      'down' :  pygame.transform.scale(pygame.image.load(self.frog_down), self.player_size)
    }

    #dict representing enemy sprites
    self.enemy_size = (16, 16)
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
        from components.player import Player
        self.player = Player((400, 300))
        self.settings = Settings()
        self.enemy_grp = pygame.sprite.Group()

        self.pos : int = 0
        self.walls = []
        self.interactabe = []
        self.maps = {}
        self.load_map("base", map_path)

    def load_all_maps(self):
        #this will loop through a file in the future and load all maps...
        #for now we can ignore
        return NotImplemented

    def load_map(self, name, filename) -> None:
        from components.enemy import Enemy, HealthBar

        surf = pytmx.load_pygame(filename)

        for layer in surf:
            if layer.name == "spawning_spaces":
                for obj in layer:
                    if obj[2] != 0:
                        #1/4 spawn rate
                        if randint(0, 4) == 0:
                            HealthBar(Enemy(self.player, (obj[0] * 16, obj[1] * 16), self.settings.enemy_sprite['fly'].convert_alpha(), 30, self.enemy_grp), self.enemy_grp)

            if layer.name == "interactables":
                for obj in layer:
                    if obj[2] != 0:
                        self.interactabe.append(pygame.Rect(obj[0] * 16, obj[1] * 16, 16, 16))


            if layer.name == "wall_collision":
                for obj in layer:
                    if obj[2] != 0:
                        self.walls.append(pygame.Rect(obj[0] * 16, obj[1] * 16, 16, 16))

        self.maps = {
            name : MapState(TiledMapData(surf), self.walls, self.interactabe, self.player, self.enemy_grp)
        }


def init_screen(width: int, height: int) -> pygame.Surface:
    screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
    return screen
