import pygame, sys
from player import Player
import pytmx
import pygame
import pyscroll
import os
import sys


class Sprite(pygame.sprite.Sprite):
    """
    Simple Sprite class for on-screen things

    """
    def __init__(self, surface) -> None:
        self.image = surface
        self.rect = surface.get_rect()


class Game:

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((1280, 720))
        self.clock = pygame.time.Clock()
        self.player = Player((640, 360))


    def run(self):
        parent_dir = os.path.dirname(os.path.dirname(__file__))
        uitImagePath = os.path.join(parent_dir, "[level tester]", "tiled info", "trial level.tmx")

        # Load TMX data
        tmx_data = pytmx.load_pygame(uitImagePath)

        # Make the scrolling layer
        map_layer = pyscroll.BufferedRenderer(
            data=pyscroll.TiledMapData(tmx_data),
            size=(400,400),
        )

        # make the pygame SpriteGroup with a scrolling map
        group = pyscroll.PyscrollGroup(map_layer=map_layer)

        # Draw map and sprites using the group
        # Notice I did not `screen.fill` here!  Clearing the screen is not
        # needed since the map will clear it when drawn

        while True:
            for event in pygame.event.get():
                self.player.input(event)
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            pygame.draw.rect(self.screen, 'red', self.player.rect)
            group.draw(self.screen)
            self.level.run()
            pygame.display.update()
            self.clock.tick(60)



if __name__ == '__main__':
    game = Game()
    game.run()

