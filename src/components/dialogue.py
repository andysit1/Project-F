import pygame as pg

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
#graph ds
class DialogueState(Dialogue):
  def __init__(self):
    super.__init__()
    self.text : str = None
    self.FONT = pg.font.SysFont(None, 24, 0)
    self.txt_graph = None

#queue ds
class DialogueStateMachcine():
  def __init__(self):
    self.q

class DialogueDisplayEngine():
  def __init__(self) -> None:
    self.engine = None
    pass

  def update(self):
    pass

  def draw(self):
    pass




'''
BRAINSTORM

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


FUTURE
 Q: How does this link with our interactables
 A: I think this method will allow for ease since we can code our interactable with a
 conditional statement on_event() to queue into a dialogue system.

 The question becomes how does our dialogue system mesh with our interactables objects???
 All interactable objects with Dialogue (DialogueState class?) should have a sequence Dialogue.

 Sequence of Dialogue should implemented in DialogueState -> graph node datastructure...

 if player collides with objects and inistance(object, Dialogueable):
    then self.dialogue.queue(objects.dialogue_sequence)

  Then the DialogueDisplayEngine will handle all the logic in the background!
'''

