import pygame
from modules.state_machine import DisplayEngine
from state.game_state import GameState
from settings import SCREEN
"""
    Starts up pygame lmao
    #hi hi hi
"""

def main():
    # Initializes all imported pygame modules
    pygame.init()
    # Start the game loop
    engine = DisplayEngine('Froggooo', 144, SCREEN[0], SCREEN[1])
    # Start the game loop with the initial state set to LoginState
    engine.run(GameState(engine))


if __name__ == "__main__":
    pygame.quit()
    main()