import pygame, sys
from level import Level
from player import Player

class Game:

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((1280, 720))
        self.clock = pygame.time.Clock()
        self.level = Level()
        self.player = Player((640, 360), self.level.all_sprites)


    def run(self):
        while True:
            for event in pygame.event.get():
                self.player.input(event)
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
            pygame.draw.rect(self.screen, 'red', self.player.rect)
            self.level.run()
            pygame.display.update()
            self.clock.tick(60)



if __name__ == '__main__':
    game = Game()
    game.run()