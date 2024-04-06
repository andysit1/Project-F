import pygame

class Level:
    def __init__(self):
        self.display_surface = pygame.display.get_surface()

        self.all_sprites = pygame.sprite.Group()

    def run(self):
        self.display_surface.fill((0, 0, 0))
        self.all_sprites.draw(self.display_surface)
        self.all_sprites.update()