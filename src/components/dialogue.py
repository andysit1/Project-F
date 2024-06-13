import pygame as pg
from queue import Queue
from treelib import Tree

import os
import sys

#needed to get modules
parent_dir = os.path.dirname(os.path.dirname(__file__))
sys.path.append(parent_dir)


from modules.state_machine import Machine
#Dialogue Specific Settings
TEXT_SPEED = 0.03

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

    self.time_delay = TEXT_SPEED #set 3 to a TIME_CONSTANT in settings.py

  def draw_border(self):
    self.surf.fill((0, 0, 255, 100))
    pg.draw.rect(self.surf, "Black", self.border_rect, 6)


  def draw(self, surface):
    self.draw_border()

    if self.index < len(self.text) - 1:
        #slows down the time of game..
        rendered_text = self.FONT.render(self.rendering, 1, 'White')
        text_rect = rendered_text.get_rect(topleft=(20, 90))

        self.surf.blit(rendered_text, text_rect)
        surface.blit(self.surf, self.textbox_rect)
        pg.display.flip()
    else:
      # draw the waiting state.. implementing later..
      pass

  def update(self, delta):
    self.time_delay -= delta * 1
    print(self.time_delay)
    if self.index < len(self.text) - 1 and self.time_delay < 0:
      self.index += 1
      self.rendering += self.text[self.index]

      self.time_delay = TEXT_SPEED


#represents the index of text and total text...
#tree ds
#has current display text and next options (Tree)
class DialogueState(Tree):
  def __init__(self):
    super().__init__()
    self.text : str = None
    self.txt_graph = None


class UserInputDialogue(DialogueState):
  def __init__(self):
    super().__init__()

  def get_options(self) -> list:
    return self.children

  def picked_option(self, identifier):
    return self.subtree(identifier=identifier)


#queue ds
class DialogueStateMachcine():
  def __init__(self):
    self.q : Queue[DialogueState] = Queue()

  def add_dialogue(self, dialogue_state : DialogueState):
    self.q.put(dialogue_state)

  def get_dialogue(self):
    return self.q.get()

  @property
  def is_q_empty(self):
    return self.q.empty


class DialogueDisplayEngine():
  def __init__(self) -> None:
    self.engine = None
    self.dialogue_machine = DialogueStateMachcine()
    self.machine = Machine()


  #prequeues the next state given
  def update(self):
    self.machine.update()

    if not self.dialogue_machine.is_q_empty():
      next_dialogue_state = self.dialogue_machine.get_dialogue()
      self.machine.next_state = next_dialogue_state

  def draw(self):
    pass


if __name__ == "__main__":
  print('Testing Tree Lib')
  tree = Tree()
  tree1= Tree()

  tree.create_node("Start", "start", data="this is the start of a dial")
  tree.create_node("No", "no", parent="start")
  tree.create_node("4", "4", parent="no")
  tree.create_node("5", "5", parent="no")
  tree.create_node("6", "6", parent="no")

  tree1.create_node("Yes", "yes")
  tree1.create_node("1", "1", parent="yes")
  tree1.create_node("2", "2", parent="yes")
  tree1.create_node("3", "3", parent="yes")


  print(tree.show(stdout=False))
  print(tree1.show(stdout=False))


  print('Dialogue System Testing')
  q : Queue[Tree]= Queue()


  d_state1 = DialogueState()
  d_state1.create_node("Hello", "root")
  d_state1.create_node("Do you want to travel", "1", parent="root")

  d_state1_1 = UserInputDialogue()
  d_state1_1.create_node("Yes", "yes")
  d_state1_1.create_node("Go to town", "1-1", "yes")
  d_state1_1.create_node("Go to house", "1-2", "yes")
  d_state1_1.create_node("Go to gym", "1-3", "yes")


  q.put(item=d_state1)
  q.put(item=d_state1_1)

  while q.not_empty:
    tmp_tree = q.get()
    print(tmp_tree.show(stdout=False))



'''"
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


Final Flow
 DialogueStates -> handles current text and dialogue options which trees will be used to represent text flow...
 DialogueStates -----> Queued into Dialogue Machine THEN
 DialogueDisplayEngine hosts Dialogue Machine which will use the current to draw the current DialogueState onto SCREEN

'''

