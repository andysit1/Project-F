import pygame as pg
import os
import sys
current_dir = os.path.dirname(__file__)
sys.path.append(current_dir)
from components.player import Player

'''
  --- UI class ---
  This class is responsible for drawing the player's information on screen.
  (ie. health bar, mana bar...)

  Functions:
    __init__ : Initializes the UI object
    on_draw : Draws the player's information
    on_event : Handles UI events
'''

#Interface class to draw the player's information!
class Interface():
  def __init__(self, player : Player):
    self.player = player

    #init variables, offset means how far from 0,0 the bars are located from
    self.h_radius = 75
    self.m_radius = 80
    self.h_offset = 15  #h = health
    self.m_offset = 20  #m = mana

    # how this works is 3.14 = 1/2 of the circle 6.28 = entire circle
    self.start_angle = 4.71
    self.end_angle = 6.28  # 1/4 circle

    # the bar difference
    self.max_arc = self.end_angle - self. start_angle

    #end angle of health
    self.h_end_angle = 0

  def on_draw(self, surface : pg.Surface):
    surface.blit(self.player.ui_pfp, (0, 0))     #draws our placeholder frog located in the top left

    pg.draw.arc(surface, "red", (-self.h_radius + self.h_offset, -self.h_radius + self.h_offset, 2 * self.h_radius, 2 * self.h_radius),
                    self.start_angle, self.h_end_angle, 4)
    pg.draw.arc(surface, "blue", (-self.m_radius + self.m_offset, -self.m_radius + self.m_offset, 2 * self.m_radius, 2 * self.m_radius),
                    self.start_angle, self.end_angle, 4)

  def on_update(self):

    h_ratio = self.player.health / self.player.max_health #percent health
    self.h_end_angle = self.start_angle + self.max_arc * h_ratio # start angle + remaining health ratio in angle


  #this handles the events of the player,
  #in the future if we want to character to blink red or something else we can code it in here...
  def on_event(self):
    pass



#represents Dialogue surface drawing logic int he game...
class Dialogue():
  def __init__(self):
    self.text = "This is just an example text to use with gradual typing."
    self.surf = pg.Surface((700,200), pg.SRCALPHA)
    self.show_textbox = False
    self.typing = False
    self.surf.fill((0, 0, 255, 100))
    self.rendering = ''
    self.FONT = pg.font.SysFont(None, 24, 0)
    self.textbox_rect = self.surf.get_rect(topleft=(150,200))
    self.border_rect = self.surf.get_rect(topleft=(0, 0))
    self.index = 0

  def draw_border(self):
    self.surf.fill((0, 0, 255, 100))
    pg.draw.rect(self.surf, "Black", self.border_rect, 6)

  def draw(self, surface, txt):
    self.draw_border()

    # if self.index > len(self.text):
      # break

    for char in txt:
        pg.time.delay(100)
        pg.event.clear()

        self.rendering = self.rendering + char
        rendered_text = self.FONT.render(self.rendering, 1, 'White')
        text_rect = rendered_text.get_rect(topleft=(20, 90))

        self.surf.blit(rendered_text, text_rect)
        surface.blit(self.surf, self.textbox_rect)
        pg.display.flip()

    self.rendering = ''


#represents the index of text and total text...
class DialogueState(Dialogue):
  def __init__(self):
    super.__init__()
    self.text : str = None
    self.FONT = pg.font.SysFont(None, 24, 0)


class DialogueDisplayEngine():
  def __init__(self) -> None:
    self.engine = None
    pass

  def update(self):
    pass

  def draw(self):
    pass




'''

Benfits by having states we can control when dialogue is played eaiser since it more
understandable and also allows us to use events to queue our dialogue into our state better

Each state might need to be init with a Dialogue System in sytem which shows all possible
Combinitions of Dialogue in current playable realam

Comp.
DState
  Represents the text in the given box...
  Might need to have auto scaling for amount of text

Machcine from state_machine
  Change to adapt a queue datastructure since we dont want to change dialogue rightawhile
  else it might look janky and probably easier to do a queue anyways since we can queue nodes
  together based on story

DialogueDisplayEngine
  Handles queue system for dialogue states.

Dialogue System
  Uses graph nodes to represent the story or dialogue with the game.
  Needs a way to read a text or json file for all text possible... later implementation..

update requirements
  settings.py
  game_state.py

{no input needed} maybe delta?
engine.update
  1. increases the index can be limited by delta to increase or slow down
  2. changes the self.render to increment up

engine.draw
  draw border and onto screen


'''

