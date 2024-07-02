

#this will be a sprite class that will handle the sprite/image of the interactable

#if we think about how a interactable should work we need to use an inheritance structure

#the difference is the sprite, radius to interact, and the result from the interaction

from typing import Any
import pygame as pg
from modules.state_machine import Machine


'''
  --- Sprite class ---
  This class is responsible for handling the basic collision logic

  Functions:
    __init__ : Initializes the UI object
    lock_on

  Usage Idea:
  You give all Interactions a reference to the player rect so we can calc the collisions. Each object
  is used to handle logic for anything that the player can do inside a game. So in the future we will use this class
  to manage our Pushable, Dialogue, and other classes
'''

class Interactions(pg.sprite.Sprite):
  def __init__(self, player, *groups) -> None:
    super().__init__(*groups)
    self.player_rect : pg.rect.Rect = player.rect
    self.image = None
    self.rect = None


  def update(self, dt):
    """
      Method called to update the state of the image
      base on what we need it might trigger it to disapear, or smth else

      Args:
          delta: The time elapsed since the last update.
    """

    if self.rect.colliderect(self.player_rect):
      self.on_event()

  def on_event(self):
    """
    Triggers the specific event given the interaction we want
    Args:
        event: The event object.
    """

    pass



class PushObject(Interactions):
  def __init__(self, player, *groups) -> None:
    super().__init__(player, *groups)
    self.vel : pg.Vector2 = None
    self.pos : pg.Vector2 = None

  def on_event(self):
    """
      set self.vel = self.player.vel
      apply the vel to the box pos

      OR

      we can treat it like moving sprite ie like the attack sprites
      then we save the position of the box based ont he self.selected_points
    """

    pass


class DialogueObject(Interactions):
  def __init__(self, player, dialogue, dialogue_machine,*groups) -> None:
    super().__init__(player, *groups)
    self.dialogue_engine = dialogue_machine
    self.dialogue = dialogue

  def on_event(self):
    self.dialogue_engine.dialogue_machine.add_dialogue(self.dialogue_test_state)
