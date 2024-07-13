
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

# from pydantic import BaseModel
# #should never handle the updates of size in here, just pure representation
# class GlowObjectModel(BaseModel):
#    loc : pg.Vector2
#    size : pg.Vector2

   #we can do some sort of validation of objects here in the future incase off screen or whatever edge case


from typing import Tuple
def to_type_vector2(self, coordinates: Tuple[int, int]):
    if len(coordinates) != 2:
        raise TypeError("Tuple size is incorrect, not 2")

    return pg.Vector2(coordinates[0], coordinates[1])

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


    # def to_rect_glow_object(self, rect_glow_objects : list[pg.Rect]):
    #    for rect in rect_glow_objects:
    #       obj = GlowObjectModel(
    #               rect.center,
    #               rect.size
    #             )
    #       self.light_cache.append(obj)

    # def to_particle_glow_object(self, particle_glow_objects : list[any]):
    #    for particle in particle_glow_objects:
    #       obj = GlowObjectModel(
    #               particle[0][0], particle[0][1],
    #               particle[]
    #             )
    #       self.light_cache.append(obj)

    # def glow_object_ADAPTER(self, glow_objects : list[any]):
    #   #passing in list[pg.Rect]
    #   if isinstance(glow_objects, list[pg.Rect]):
    #      self.to_rect_glow_object(rect_glow_objects=glow_objects)

    #   #passing in Particles
    #   if len(glow_objects[0]) == 3: #TODO make particle class for now use len of 3 since  # particle = [loc, velocity, timer]
    #      pass

    def set_rect_glow_objects(self, rect_group : list[pg.Rect]):
      #adapter here
      self.light_cache += rect_group

      size_of_glow = self.glow_cache.keys()
      #INIT dict keys with new sizes
      for rect in rect_group:
          if rect.size not in size_of_glow:
            self.glow_cache[rect.size] = None #instead of size we should use a string representing size * color ()

      self.create_glow_surface_cache()
      print("size of glow", len(size_of_glow))
    #SET reference to list of rects

      #adapter here
    def set_particle_glow_objects(self, particle_group : list[pg.Rect]):
      self.light_cache += particle_group
      size_of_glow = self.glow_cache.keys()
      #INIT dict keys with new sizes
      # for particle in particle_group:


      self.create_glow_surface_cache()
      print("size of glow", len(size_of_glow))
    #SET reference to list of rects

    # def set_glow_objects(self, glow_group : list[any]):
    #   self.create_glow_surface_cache()
    #   print("size of glow", len(size_of_glow))
    #draw the light surface (


    def draw_rect_glow_objects(self, surface, rects : list[pg.Rect]):
        for rect_obj in rects:
          #make it proportional to time is the radius
          radius = 40
          surface.blit(circle_surf(radius, (20, 20, 60)), (int(rect_obj[0][0] - radius), int(rect_obj[0][1] - radius)), special_flags=pg.BLEND_RGB_ADD)


    def draw(self, surface : pg.Surface , glow_objs : list[any]):
      if glow_objs:
        if isinstance(glow_objs, list) and isinstance(glow_objs[0], pg.Rect):
          self.draw_rect_glow_objects(surface=surface, rects=glow_objs)

        if len(glow_objs[0]) == 3:
          for particle in glow_objs:
              radius = particle[2] * 2

              pg.draw.circle(surface, (255, 255, 255), [int(particle[0][0]), int(particle[0][1])], int(particle[2]))
              surface.blit(circle_surf(radius, (20, 20, 60)), (int(particle[0][0] - radius), int(particle[0][1] - radius)), special_flags=pg.BLEND_RGB_ADD)


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
