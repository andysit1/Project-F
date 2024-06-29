import pygame
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
from random import randint

current_dir = os.path.dirname(os.path.dirname(__file__))
uitImagePath = os.path.join(current_dir,"[level tester]", "trial_blue", "unbound_blue.tmx")
dialoguePath = os.path.join(current_dir, "dialogues", "tree_test.json")
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

        self.is_map_toggle : bool = False

        #MINI MAP INIT
        self.mini_group : PyscrollGroup = PyscrollGroup(map_layer=self.map_layer, default_layer=1)
        self.mini_group.add(self.player)

        self.mini_map = pygame.Surface((SCREEN[0], SCREEN[1]))
        self.mini_map.set_alpha(220)
        self.mini_map.set_colorkey((0,0,0))




    def set_toggle(self):
        self.is_map_toggle = not self.is_map_toggle

    def on_draw(self, surface : pygame.Surface, center):
        self.map_layer.zoom = 5
        self.group.center(value=center)
        self.group.draw(surface=surface)

        if self.is_map_toggle:
            #Note: we should limit the player movements at this point so they cant just play in a more zoomed out fov
            self.map_layer.zoom = 2
            self.mini_group.center(value=center)
            self.mini_group.draw(surface=self.mini_map)
            surface.blit(self.mini_map, (10, 10))

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
        self.interactables = []
        self.maps = {}
        self.load_map("base", map_path)
        self.load_map("next_map", map_path)

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
                        self.interactables.append(pygame.Rect(obj[0] * 16, obj[1] * 16, 16, 16))


            if layer.name == "wall_collision":
                for obj in layer:
                    if obj[2] != 0:
                        self.walls.append(pygame.Rect(obj[0] * 16, obj[1] * 16, 16, 16))


        # i have to use interactables as the name as the unbounded blue uses this variable. I forgot is it causes problems else where
        # got to ask luca later to make sure this grammar mistake won't cause issues in the future

        self.maps[name] = MapState(TiledMapData(surf), self.walls, self.interactables, self.player, self.enemy_grp)




def init_screen(width: int, height: int) -> pygame.Surface:
    screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
    return screen


import json


def read_json_tree(info : dict):
    options = info.keys()
    print("All options", options)
    for key in info.keys():
        print(key, info[key])
        read_json_tree(info[key]['children'])



'''
    1.) Create a function to take a node and when hit/triggered then it will call
    the tree to get the next iterations of questions. I ideally we need to check two cases

        if childen > 1
            then we display options ie user input

        if childen == 1
            queue/get the next input

        if no childen
            do nothing since the queue empty it sell
'''

def get_dialogue(nid : int):
    #2 is the children and + ranch combination.
    childs : Node = tree.children(nid=nid + 1)

    for child in childs:
        if child.tag != "Node":
            print(child.tag, childs)

        if child.tag == "Node":
            get_dialogue(child.identifier)

        if child.tag == "data":
            get_dialogue(child.identifier)




if __name__ == "__main__":
    print("testing dialogue json")
    with open(dialoguePath) as f:
        data = json.load(f)

    from modules.treelib_utils import json_2_tree
    from treelib import Tree, Node

    tree : Tree = json_2_tree(data , verbose=True, listsNodeSymbol=None)
    tree.show()

    while True:
        start = tree.get_node(1)
        # if len(child) > 2:
        #     print("Wrong layer")
        #     print(child)
        #     break


        get_dialogue(1)
                #pick here...

        break


    # read_json_tree(data)



