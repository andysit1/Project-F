import pygame
from modules.state_machine import DisplayEngine
from state.game_state import GameState

"""
    Starts up pygame lmao
    #hi hi hi
"""

def main():
    # Initializes all imported pygame modules
    pygame.init()
    # Start the game loop
    engine = DisplayEngine('Froggooo', 144, 1280, 720)
    # Start the game loop with the initial state set to LoginState
    engine.run(GameState(engine))

pygame.quit()
main()