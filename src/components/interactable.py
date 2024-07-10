

#this will be a sprite class that will handle the sprite/image of the interactable

#if we think about how a interactable should work we need to use an inheritance structure

#the difference is the sprite, radius to interact, and the result from the interaction

from typing import Any
import pygame as pg


'''
  --- Interactions class ---
  This class is responsible for handling the basic collision logic

  Functions:
    __init__ : Initializes the UI object



  Usage Idea:
  You give all Interactions a reference to the player rect so we can calc the collisions. Each object
  is used to handle logic for anything that the player can do inside a game. So in the future we will use this class
  to manage our Pushable, Dialogue, and other classes
'''

class Interactions(pg.sprite.Sprite):
  def __init__(self, entity, *groups) -> None:
    super().__init__(*groups)
    self.entity = entity
    self.entity_rect : pg.rect.Rect = entity.rect
    self.image = None
    self.rect = None

  #this is a useful function to know if an entity is going towards or away for more specific interactions
  @classmethod
  def is_moving_towards(self):
    pos = self.entity.pos

    center = pg.Vector2(self.rect.centerx, self.rect.centery)
    next_step = pos + self.entity.vel

    #if the next step given the current vel is closer to the center of an object(pushing against) then this means we are going towards
    #else then we are going away
    if center.distance_to(next_step) < center.distance_to(pos):
      return True
    else:
      return False



  def update(self, dt):
    """
      Method called to update the state of the image
      base on what we need it might trigger it to disapear, or smth else

      Args:
          delta: The time elapsed since the last update.
    """

    if self.rect.colliderect(self.entity_rect):
      self.on_event()

  def on_event(self):
    """
    Triggers the specific event given the interaction we want
    Args:
        event: The event object.
    """

    pass


'''
  --- PushObject class ---
  This class is responsible for handling the basic pushing logic

  Idea:
  In real life when we push objects the force which we apply will alway apply back in equal force,
  this means that we need to code walls ingame/other objects that can move to shoot an object force backwards

'''

class WallObject(Interactions):
  def __init__(self, entity, *groups) -> None:
    super().__init__(entity, *groups)

  def on_event(self):

    if self.is_moving_towards:
      self.entity -= self.entity.vel  #whenever is hit whether, pushobject or player object we apply the negative vel vectors backwards

    return super().on_event()

'''
  --- PushObject class ---
  This class is responsible for handling the basic pushing logic

  Idea:
  In real life when we push objects the force which we apply will alway apply back in equal force,
  this means that we need to code walls ingame/other objects that can move to shoot an object force backwards

'''

class PushObject(Interactions):
  def __init__(self, entity, *groups) -> None:
    super().__init__(entity, *groups)
    self.vel : pg.Vector2 = None
    self.pos : pg.Vector2 = None

  def on_event(self):
    #push object
    self.pos += self.entity.vel
    self.rect.center = self.pos



class DialogueObject(Interactions):
  def __init__(self, player, dialogue, dialogue_machine,*groups) -> None:
    super().__init__(player, *groups)
    self.dialogue_engine = dialogue_machine
    self.dialogue = dialogue

  def on_event(self):
    self.dialogue_engine.dialogue_machine.add_dialogue(self.dialogue_test_state)
