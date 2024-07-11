
"""
How it works

In game there will be glowable objects which will have a glow_setting

player will check for glowable objects within x distance from player.pos (a little more than resolution) (x distance)
    cool idea cause we can set a specific glow distance given tongue distance and if close to tongue objects glow

we will have a cache for all glow surfaces given a size to reduce surface generation

on update -> pass the glowable objects rects to light manager
on_draw -> draws all lighting objects based on translation func and if they are within range
          then we apply lighting surface with blend mode before drawing ui component
"""


class LightingManager():
    def __init__(self):
      self.light_cache = ()

    def glow_color(self, pos, size, color):
      pass



