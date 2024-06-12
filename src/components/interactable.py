

#this will be a sprite class that will handle the sprite/image of the interactable

#if we think about how a interactable should work we need to use an inheritance structure

#the difference is the sprite, radius to interact, and the result from the interaction

import pygame as pg
from .ui import DialogueState


class Interactable(pg.sprite.Sprite):
  def __init__(self, *groups) -> None:
    super().__init__(*groups)

  def update(self, dt):
    """
      Method called to update the state of the image
      base on what we need it might trigger it to disapear, or smth else

      Args:
          delta: The time elapsed since the last update.
    """
    pass

  def on_event(self):
    """
    Method called when an event occurs.
    Might trigger dialouge system
    Might trigger item drop
    Might trigger health increase not sure yet

    Args:
        event: The event object.
    """

    pass


class Interactable_Dialogueable(DialogueState):
  def __init__(self):
    super().__init__()