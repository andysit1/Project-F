import pygame as pg
import pytmx
from pyscroll.data import TiledMapData
from pyscroll.orthographic import BufferedRenderer
from pyscroll.group import PyscrollGroup
from settings import SCREEN

class PlayerMap:

    def __init__(self, map_file):
        # set map to closed by default
        self.is_open = False
        self.tint_color = (0, 0, 0, 150)
        self.map_scale = 0.25  # Scale down the map to 25% of the screen size

        # Load the map
        tmx_data = pytmx.load_pygame(map_file)
        map_data = TiledMapData(tmx_data)
        self.map_layer = BufferedRenderer(map_data, size=SCREEN)
        self.map_layer.zoom = 2.5
        self.group = PyscrollGroup(map_layer=self.map_layer, default_layer=2)

        # Create a smaller surface for the map
        self.map_surface_size = (int(SCREEN[0] * self.map_scale), int(SCREEN[1] * self.map_scale))
        self.map_surface = pg.Surface(self.map_surface_size)

    def toggle_map(self):
        # invert map state and print its status
        self.is_open = not self.is_open
        print("map", self.is_open)

    def draw(self, surface):
        # only draw map shit when its toggled on
        if self.is_open:
            # BG
            # create surface with same size as screen - fill it with BG color - blit
            tint_surface = pg.Surface(surface.get_size(), pg.SRCALPHA)
            tint_surface.fill(self.tint_color)
            surface.blit(tint_surface, (0, 0))

            # MAP
            self.map_surface.fill((0, 0, 0, 0))  # Clear the map surface
            self.group.draw(self.map_surface)   # Draw the map onto the smaller surface

            # Blit the smaller map surface onto the center of the main surface
            map_rect = self.map_surface.get_rect(center=surface.get_rect().center)
            surface.blit(self.map_surface, map_rect.topleft)
