
"""
How it works

In game there will be glowable objects which will have a glow_setting

player will check for glowable objects within x distance from player.pos (a little more than resolution) (x distance)
    cool idea cause we can set a specific glow distance given tongue distance and if close to tongue objects glow

we will have a cache for all glow surfaces given a size to reduce surface generation

on update -> pass the glowable objects rects to light manager
on_draw -> draws all lighting objects based on translation func and if they are within range
          then we apply lighting surface with blend mode before drawing ui component

FOR NOW LETS JUST DO CIRCLE GLOW OBJECTS


"""


import pygame as pg

#fluffy potato code
def circle_surf(radius, color):
    surf = pg.Surface((radius * 2, radius * 2))
    pg.draw.circle(surf, color, (radius, radius), radius)
    surf.set_colorkey((0, 0, 0))
    return surf


class LightingManager():
    def __init__(self):
      self.light_cache : list[pg.Rect] = []
      self.glow_cache = dict()
      self.light_layer : pg.Surface = pg.Surface((1920, 1080), pg.SRCALPHA)

    def create_glow_surface_cache(self):
      for keys in self.glow_cache.keys():
        if self.glow_cache[keys] == None:
          self.glow_cache[keys] = circle_surf(keys[0] * 2, (20, 20, 60))
      print(len(self.glow_cache))

    #SET reference to list of rects
    def set_glow_objects(self, glow_group : list[pg.rect.Rect]):
      self.light_cache += glow_group
      size_of_glow = self.glow_cache.keys()
      #INIT dict keys with new sizes
      for rect in glow_group:
          if rect.size not in size_of_glow:
            self.glow_cache[rect.size] = None #instead of size we should use a string representing size * color ()

      self.create_glow_surface_cache()
      print("size of glow", len(size_of_glow))

    #draw the light surface (
    def draw(self, surface : pg.Surface):
      for obj in self.light_cache:
        self.light_layer.blit(self.glow_cache[obj.size], (obj.centerx - obj.width * 2, obj.centery - obj.height * 2),  special_flags=pg.BLEND_RGB_ADD)
      surface.blit(self.light_layer, (0, 0))



"""
FLOW

lm.set_glow_objects(pygame group of sprites)

  loop through and grab size of all rects and push to set if we have multiple of the same glow size then it doesnt matter



"""


if __name__ == "__main__":

  import unittest

  # Assuming LightingManager class and circle_surf function are defined here as provided

  class TestLightingManager(unittest.TestCase):
      def setUp(self):
          pg.init()
          self.lighting_manager = LightingManager()

      def test_initialization(self):
          self.assertIsInstance(self.lighting_manager.light_cache, list)
          self.assertIsInstance(self.lighting_manager.glow_cache, dict)
          self.assertIsInstance(self.lighting_manager.light_layer, pg.Surface)
          self.assertEqual(self.lighting_manager.light_layer.get_size(), (1920, 1080))
          self.assertEqual(self.lighting_manager.light_layer.get_flags() & pg.SRCALPHA, pg.SRCALPHA)


      def test_rect_cache(self):
        #start 10 objects in cache
        rect_group = []
        for i in range(10):
          rect_group.append(pg.rect.Rect(i, i, i, i))
        self.lighting_manager.set_glow_objects(rect_group)

        #should only add 5 objects cause cache
        rect_group = []
        for i in range(5, 15):
          rect_group.append(pg.rect.Rect(i, i, i, i))
        self.lighting_manager.set_glow_objects(rect_group)

  if __name__ == '__main__':
      unittest.main()
