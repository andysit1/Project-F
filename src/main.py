import pygame
from modules.state_machine import DisplayEngine
from state.game_state import GameState

"""
    Starts up pygame lmao
"""

def main():
    # Initializes all imported pygame modules
    pygame.init()

    # Create a DisplayEngine object with the specified title, frame rate, and window size
    engine = DisplayEngine('Froggooo', 144, 800, 600)

    # Start the game loop
    engine = DisplayEngine('Froggooo', 50, 1280, 720)
    # Start the game loop with the initial state set to LoginState
    engine.run(GameState(engine))


pygame.quit()
main()