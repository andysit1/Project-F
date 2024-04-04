"""
This module provides classes for creating a simple game engine using Pygame.

Classes:
    State: Represents a game state.
    Machine: Manages transitions between different game states.
    DisplayEngine: Manages the main game loop and display functionality.
"""

import pygame
import time

#update with chunking for future mapping
class State():
    """
    Represents a game state interface.

    Attributes:
        engine: The game engine associated with the state.
    """

    def __init__(self, engine):
        """
        Initialize a State object.

        Args:
            engine: The game engine associated with the state.
        """
        self.engine = engine
    def on_draw(self, surface):

        """
        Method called when the state needs to be drawn on the screen.

        Args:
            surface: The surface to draw on.
        """
        pass

    def on_event(self, event):
        """
        Method called when an event occurs.

        Args:
            event: The event object.
        """
        pass

    def on_update(self, delta):
        """
        Method called to update the state.

        Args:
            delta: The time elapsed since the last update.
        """
        pass

    def handle_movement(self, event, delta):

        """
        Method to handle movement within the state.
        """
        pass

class Machine:
    """
    Manages transitions between different game states.
    """
    def __init__(self):
        """
        Initialize a Machine object.
        """
        self.current = None
        self.next_state = None

    def update(self):
        """
        Update the current state.
        """
        if self.next_state:
            self.current = self.next_state
            self.next_state = None

class DisplayEngine:
    """
    Manages the main game loop and display functionality.
    """
    def __init__(self, caption, fps, width, height, flags=0):
        """
        Initialize a DisplayEngine object.

        Args:
            caption: The caption for the game window.
            fps: The target frames per second.
            width: The width of the game window.
            height: The height of the game window.
            flags: Additional flags for the game window (default is 0).
        """
        pygame.display.set_caption(caption)
        self.surface = pygame.display.set_mode((width, height), flags)
        self.rect = self.surface.get_rect()
        self.clock = pygame.time.Clock()
        self.running = True
        self.delta = 0
        self.fps = fps

        self.machine = Machine()

    def loop(self):
        """
        Main game loop which handles all draw, update, on_event, and movement
        """
        previous_time = time.time()
        while self.running:
            dt = time.time() - previous_time
            previous_time = time.time()
            self.machine.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                else:
                    self.machine.current.on_event(event)

            self.machine.current.on_draw(self.surface)
            self.machine.current.on_update(dt)

            try:
                self.machine.current.handle_movement(event=None, delta=dt)
            except:
                pass

            pygame.display.flip()
            self.delta = self.clock.tick(self.fps)


    def run(self, state):
        self.machine.current = state
        self.loop()

