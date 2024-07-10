


'''
  --- Base_Sprite class ---
  This class is responsible making a base class so that it makes creating new objects and game
  entities a lot easier.

  Issue: Right now we have to deal with position and how it deals with zoom. Instead I want to have a
  sprite class that can have the basic methods ie like make_transparent,lock on sprite and much more to save time
  and recoding a lot of the annoying logic

  Functions:
    __init__ : Initializes the UI object
    make_transparent : Draws sprite to be visible
    make_visible : Draws the sprite to be not visible
'''
import pygame as pg
from modules.state_machine import Machine

#handles base functions for all sprites
class Base_Sprite(pg.sprite.Sprite):
  def __init__(self, *groups) -> None:
    super().__init__(*groups) #puts this sprite into this group..
    self.is_visible = False #assume all sprites should be transparent on launch..
    self.sprite_machine = Machine()
    self.image = None
    self.rect = None

  def make_transparent(self):
    self.is_visible = False
    self.image.set_alpha(0)

  def make_visible(self):
    self.is_visible = True
    self.image.set_alpha(255)

'''
  --- Sprite class ---
  This class is responsible for making positioning easier.

  Functions:
    __init__ : Initializes the UI object
    lock_on
'''
from components.player import Player

class Moving_Sprite(Base_Sprite):
  def __init__(self, focus,*groups) -> None:
    super().__init__(*groups)
    self.focus : Player = focus
    self.reference_points = {
      'center' : None,
      'left' : None,
      'right' : None,
      'up' : None,
      'down' : None
    }
    self.selected_point = 'right'
    self.horizontal_surface = pg.Surface([30, 5]).convert()
    self.vertical_surface = pg.Surface([5, 30]).convert()

    self.image = self.horizontal_surface
    self.make_visible()
    self.rect = self.image.get_rect()
    self.pos_rect = pg.Rect(0, 0, 5, 5)
    self.offset = 15
    self.horizontal_vertical = 0 #0 - horizontal, #1 - vertical

  def set_selected_points(self, direction):
    if direction not in self.reference_points.keys():
      TypeError("Direction not found in possible reference points.")

    self.selected_point = direction

  #calculates the position base on center
  def update_reference_points(self):
    current_position = self.focus.rect.center
    self.reference_points['center'] = current_position
    self.reference_points['left'] = (current_position[0] - self.offset, current_position[1])
    self.reference_points['right'] = (current_position[0] + self.offset, current_position[1])
    self.reference_points['up'] = (current_position[0], current_position[1] - self.offset)
    self.reference_points['down'] = (current_position[0], current_position[1] + self.offset)

  #helper functions
  def change_vertical_surface(self):
    self.image = self.vertical_surface
    self.rect = self.image.get_rect()
    self.horizontal_vertical = 1

  def change_horizontal_surface(self):
    self.image = self.horizontal_surface
    self.rect = self.image.get_rect()
    self.horizontal_vertical = 0

  #changes the surface base on what we need
  def update_surface_directionality(self):
    self.selected_point = self.focus.direction
    if self.selected_point in ('left', 'right') and self.horizontal_vertical == 1:
      self.change_horizontal_surface()
    elif self.selected_point in ('up', 'down') and self.horizontal_vertical == 0:
      self.change_vertical_surface()

  #updates the direction of the attacks
  def align(self):
    self.update_surface_directionality()

    if self.selected_point == "right":
      self.rect.midleft = self.pos_rect.midleft
    elif self.selected_point == "left":
      self.rect.midright = self.pos_rect.midright
    elif self.selected_point == "up":
      self.rect.midbottom = self.pos_rect.midtop
    elif self.selected_point == "down":
      self.rect.midtop = self.pos_rect.midbottom


  #clips our reference points with our spite
  def update_sprites_directions_and_reference_points(self):
    self.update_reference_points()
    self.pos_rect.centerx = self.reference_points[self.selected_point][0]
    self.pos_rect.centery = self.reference_points[self.selected_point][1]
    self.align()


  def update(self, dt):
    self.update_sprites_directions_and_reference_points()



