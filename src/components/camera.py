import pygame as pg
from pygame.math import Vector2
from components.player import Player

#binds to player -> focuses on player or maybe an object?!?!

# This is the camera class handles the position of surface we see on the world surface
class Camera:
    def __init__(self, focus):
        #focus/lock on player
        self.focus : Player = focus
        self.view : pg.Surface = pg.display.set_mode((800, 600))
        self.origin = Vector2(800 // 2, 600 //2)
        self.viewP = self.origin.copy()

    def viewpointPosition(self):
        # Calculate the difference between the player and the center of the screen
        heading = self.focus.pos - self.origin
        # Move the camera gradually towards the player
        self.origin += heading * 0.05
        return -self.origin + Vector2(800 // 2, 600 // 2)
