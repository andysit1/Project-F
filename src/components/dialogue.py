import pygame as pg
from queue import Queue
from treelib import Tree

import os
import sys

#needed to get modules
parent_dir = os.path.dirname(os.path.dirname(__file__))
sys.path.append(parent_dir)

from modules.state_machine import Machine, DisplayEngine
from pydantic import BaseModel



#DIALOGUE MODELS FOR STORING
'''
BRAINSTORM

There are two types of Dialogues in game one where we have
 1.) back to back no interaction from userinput ie like a monologue
 2.) we need user input so decisions are at play which dictate the game...
    Originally we could just use the tree nodes and see if the tree nodes child > 1.
'''

from pydantic import BaseModel, Field
from typing import List, Optional

#ALL DIALOGUE is mono for now until we want to make a more complex dialogue system...
class DialogueJSON(BaseModel):
    node_type : str = "read"
    id: int = Field(..., example=1, description="Unique identifier for the dialogue entry")
    text: str = Field(..., example="Hello, how are you?", description="Current dialogue text")
    #added for now cause maybe in the future we might want to do something with this... can ignore
    speaker: Optional[str] = Field(None, example="Alice", description="Speaker of the current dialogue text")

#represents the parent and child of the dialogue for ONE level
class TreeNodeDialogueJSON(BaseModel):
    node_type : str = "input"
    dialogue : DialogueJSON
    child_dialogue : Optional[list]

    def add_child_node(self, node):
      self.child_dialogue.append(node)

    def on_load_json(self, filename):
      pass

    def convert_data_dialogue_nodes(self):
      pass


# Example usage
example1_dialogue = DialogueJSON(
    id=1,
    text="Hello, how are you?",
    speaker="Alice",
)

example2_dialogue = DialogueJSON(
    id=2,
    text="I'm good, thanks! How about you?",
    speaker="Bob",
)

# Example usage
example3_dialogue = DialogueJSON(
    id=3,
    text="I'm great cause I'm coding today",
    speaker="Alice",
)

dia3 = DialogueJSON(
    id=4,
    text="let's go down a level",
    speaker="Alice",
)

node2 = TreeNodeDialogueJSON(dialogue=dia3, child_dialogue=[])

node1 = TreeNodeDialogueJSON(dialogue=example1_dialogue, child_dialogue=[])
node1.add_child_node(example2_dialogue)
node1.add_child_node(example3_dialogue)
node1.add_child_node(node2)


#DIALOGUE INGAME LOGIC
#Dialogue Specific Settings
TEXT_SPEED = 0.03

class _DialogueStateMachine(Machine):
  def __init__(self):
    self.current : DialogueState = None
    self.next_state : DialogueState = None


  def update(self):
    try:
      if self.next_state:
        self.current = self.next_state
        self.next_state = None
    except:
      print("ERROR SWITCHING")
      pass


#represents Dialogue surface drawing logic int he game...
class Dialogue():
  def __init__(self, text : str = "This is just an example text to use with gradual typing."):
    self.text = text
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

  @property
  def is_done(self):
    if self.index == len(self.text) - 1:
      return True
    else:
      return False

  def draw(self, surface):
    self.draw_border()

    rendered_text = self.FONT.render(self.rendering, 1, 'White')
    text_rect = rendered_text.get_rect(topleft=(20, 90))

    self.surf.blit(rendered_text, text_rect)
    surface.blit(self.surf, self.textbox_rect)
    pg.display.flip()


  def update(self, delta):
    self.time_delay -= delta * 1
    if self.index < len(self.text) - 1 and self.time_delay < 0:
      self.rendering += self.text[self.index]
      self.index += 1

      self.time_delay = TEXT_SPEED


#represents the index of text and total text...
#tree ds
#has current display text and next options (Tree)
class DialogueState(Tree):
  def __init__(self, text : str = None):
    super().__init__()
    self.done : bool = False
    self.dialogue : Dialogue = Dialogue(text)
    self.txt_graph = None

  #kinda reundant but we can remove later..
  @property
  def is_done(self):
    return self.dialogue.is_done

#queue ds
class DialogueStateMachine():
  def __init__(self):
    self.q : Queue[DialogueState] = Queue()

  def add_dialogue(self, dialogue_state : DialogueState):
    self.q.put(dialogue_state)

  def get_dialogue(self):
    try:
      if self.q.qsize() != 0:
        temp_state = self.q.get()
        # print(temp_state, temp_state.dialogue.text)
        return temp_state
      else:
        print("q is empty")
    except:
      print("Error...")

    return None


  @property
  def is_q_empty(self):
    return self.q.empty

class DialogueDisplayEngine():
  def __init__(self, engine) -> None:
    self.engine : DisplayEngine = engine
    self.dialogue_machine = DialogueStateMachine()
    self.machine = _DialogueStateMachine()

  def set_current(self, state : DialogueState):
    self.machine.current = state

  def set_next(self, state : DialogueState):
    self.machine.next_state = state

  def update(self, delta):
    #updates the timers for dialogue
    if self.machine.current:
      self.machine.current.dialogue.update(delta)

    if not self.dialogue_machine.q.empty():
      #if non and we have dialogue then we want to set/start the queue to read...
      if self.machine.current == None:
        tmp_dialogue = self.dialogue_machine.get_dialogue()
        self.set_next(tmp_dialogue)
      else:
        #check to see if the text is done so we can swap to new screen
        try:
          if self.machine.current.dialogue.is_done:
            tmp_dialogue = self.dialogue_machine.get_dialogue()
            if tmp_dialogue:
              self.set_next(tmp_dialogue)
        except:
          pass
        #if we have something on screen and

    self.machine.update()

  def draw(self):
    try:
      if self.machine.current.dialogue:
        self.machine.current.dialogue.draw(self.engine.surface)
    except:
      pass


if __name__ == "__main__":
  # print("Testing DialogueJson Implementation")
  # print(node1.model_dump_json())

  print('Testing Tree Lib')
  tree = Tree()

  tree.create_node("Start", "start", data="this is the start of a dial")
  tree.create_node("No", "no", parent="start")
  tree.create_node("4", "4", parent="no")
  tree.create_node("5", "5", parent="no")
  tree.create_node("6", "6", parent="no")

  tree.create_node("Yes", "yes", parent="start")
  tree.create_node("1", "1", parent="yes")
  tree.create_node("2", "2", parent="yes")
  tree.create_node("3", "3", parent="yes")


  print(tree.show(stdout=False))
  tree.save2file("tree_test.txt")
  print(tree.to_json(with_data=True))

  # print('Dialogue System Testing')
  # q : Queue[Tree]= Queue()


  # d_state1 = DialogueState()
  # d_state1.create_node("Hello", "root")
  # d_state1.create_node("Do you want to travel", "1", parent="root")

  # d_state1_1 = DialogueState()
  # d_state1_1.create_node("Yes", "yes")
  # d_state1_1.create_node("Go to town", "1-1", "yes")
  # d_state1_1.create_node("Go to house", "1-2", "yes")
  # d_state1_1.create_node("Go to gym", "1-3", "yes")


  # engine.draw()

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

