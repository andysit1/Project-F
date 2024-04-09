import pygame
import sys
import os
import json
from pydantic import BaseModel
from modules.utils import load_settings, save_settings


# Setup the environment by appending the current directory to the system path for asset access.
current_dir = os.path.dirname(os.path.dirname(__file__))
sys.path.append(current_dir)


#Needs discussion about which settings we want to track...
class SettingsModel(BaseModel):
  def __init__(self):
     pass


class Settings():
  """
    A class to manage and provide settings and assets for the game, such as player ships, backgrounds, level-up screens, game over screens, and projectiles.

  """
  def __init__(self):
    """
    Initializes the Settings class by loading all necessary game assets from the assets directory and creating theme sets.
    """
    # Paths for various game assets are constructed here using `os.path.join`
    self.frog_right  = os.path.join(current_dir, "assets", "player_assets", "right.png")
    self.frog_left  = os.path.join(current_dir, "assets", "player_assets", "left.png")
    self.frog_up  = os.path.join(current_dir, "assets", "player_assets", "up.png")
    self.frog_down  = os.path.join(current_dir, "assets", "player_assets", "down.png")


    #dict representing frog sprites
    self.character_sprite = {
      'right' : pygame.image.load(self.frog_right),
      'left' : pygame.image.load(self.frog_left),
      'up' : pygame.image.load(self.frog_up),
      'down' : pygame.image.load(self.frog_down)
    }

if __name__ == "__main__":
  #example of how it works
  settings = Settings()
  print("Parent directory...", current_dir)
  print("frog right path", settings.frog_right)
  print("RIGHT SURF", settings.character_sprite['right'])