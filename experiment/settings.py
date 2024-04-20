import pygame
import sys
import os
from pydantic import BaseModel
from modules.utils import load_settings, save_settings


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
    self.player_size = (30, 30)
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

if __name__ == "__main__":
  #example of how it works
  settings = Settings()
  print(settings.character_sprite)
  print(settings.src)
  print(settings.enemy_sprite)