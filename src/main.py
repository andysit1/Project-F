import pygame
import os
import sys
# Setup the environment by appending the current directory to the system path.
current_dir = os.path.dirname(__file__)
sys.path.append(current_dir)
from modules.state_machine import DisplayEngine
from state.gameState import GameState


#hello poo

def main():
    """
    The main function that initializes the pygame environment, sets up the game engine, and starts the game loop.

    This function creates an instance of the DisplayEngine, sets the initial state to LoginState, and runs the game loop
    until the game dis exited. Pygame is initialized at the beginning and quit at the end to ensure proper resource management.
    """
    pygame.init()# Initialize all imported pygame modules
    # Create a DisplayEngine object with the specified title, frame rate, and window size
    engine = DisplayEngine('Froggooo', 144, 800, 600)
    # Start the game loop with the initial state set to LoginState
    engine.run(GameState(engine))
pygame.quit()

main()