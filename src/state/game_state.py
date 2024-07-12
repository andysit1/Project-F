import pygame as pg
from random import randrange
from pygame.math import Vector2
from modules.state_machine import State, Machine
from components.player import Player
from components.enemy import Enemy, HealthBar
from components.ui import Interface
from components.camera import Camera
from settings import Settings, MapSettings
from components.particles import ParticleGenerator
from components.attack import AttackSprite
from components.attack import SweepAttackSprite
from modules.state_machine import Machine


'''
  --- GameState class ---
  This class is responsible for managing the game state, which includes everything currently loaded into the game.
  (ie. everything not in the main menu, settings...)
  (ie. the player, enemies, background...)

  Functions:
    __init__ : Initializes the game state
    on_draw : Draws the game state
    on_event : Handles game state events (ie. key presses)
    on_update : Updates game state information each frame/update
'''

class GameState(State):
  def __init__(self, engine):
    super().__init__(engine)
    self.settings = Settings()               #init pygame surfaces

    self.dt = 0                              # Initializes delta time
    self.clock = pg.time.Clock()             # Needed clock thing?
    font = pg.font.SysFont('comicsans', 15)  # Initializes font

    self.map_settings = MapSettings()        #init map settings
    self.map_machine = Machine()
    self.map_machine.current = self.map_settings.maps.get("base") #set the first state as base

    self.player = self.map_machine.current.player
    self.enemy_group = self.map_machine.current.enemy_grp

    self.ui = Interface(self.player)
    self.camera_view = Camera(self.player)
    self.particle_gen = ParticleGenerator() #TODO update the

    #THIS must be moved to player since when map states are swaped we lose the group and our attacks box is lost
    # self.attack_sprite_test = PierceGrappleAttack(self.player, self.map_machine.current.group)
    self.attack_sprite_test = AttackSprite(self.player, self.map_machine.current.group)

    self.attack_sweep = SweepAttackSprite(self.player, self.map_machine.current.group)



  #changes the player position and next map state...
  def on_swap_map_state(self):
    self.map_machine.next_state = self.map_settings.maps.get("next_map")
    self.map_machine.next_state.player.set_player_pos(pg.Vector2((100, 600)))

  def on_draw(self):
    view = -self.camera_view.viewpointPosition() + self.player.pos
    self.map_machine.current.on_draw(self.engine.surface, view)

    world_to_camera = self.map_machine.current.map_layer.translate_points
    self.player.on_draw_player_sprites(self.engine.surface, world_to_camera)

    #draws the ui onto the camera surface so it doesn't get effected by the offset
    self.ui.on_draw(self.engine.surface)
    pg.draw.circle(self.engine.surface, "white", (int(self.player.pos.x), int(self.player.pos.y)), 5)

  def on_event(self, event):
    #handles the logic of player to player events
    self.player.handle_event(event=event, dt=self.dt)

    #handles gamestate to player interactions
    if event.type == pg.KEYDOWN:
      if event.key == pg.K_SPACE:
        self.player.attack_sweep.handle_attack_input(self.enemy_group)
      elif event.key == pg.K_c:
        self.player.attack_sprite_test.perform_tongue(self.enemy_group)


  def update_sprites_collisions_to_walls(self, dt):
    return [sprite.move_back(dt) for sprite in self.map_machine.current.group.sprites() if getattr(sprite, "feet", None) and sprite.feet.collidelist(self.map_machine.current.walls) > -1]



  """
  Yon can use is_tongue_collisions_to_anything_rectable for anything but I think the two functions below make the functions easier to read and isolates the logic better
  Choice is up to you.
  """

  #you can probably optimize these calls to check for 


  def is_tongue_collisions_to_anything_rectable(self, collisions_rect : list[pg.Rect]) -> list[pg.Rect]:
    if self.player.is_tongue_out():
      collisions_rects = [rect for rect in collisions_rect if rect.collidepoint(self.player.tongue_points[-1]) == True]
      return collisions_rects

  def is_tongue_collisions_to_walls(self) -> bool:
    if self.player.is_tongue_out():
      walls = [wall for wall in self.map_machine.current.walls if wall.collidepoint(self.player.tongue_points[-1]) == True]
      if len(walls) > 0:
        return True
    return False

  def is_tongue_collisions_to_enemys(self) -> bool:
    if self.player.is_tongue_out():
      enemys = [enemy for enemy in self.enemy_group if enemy.rect.collidepoint(self.player.tongue_points[-1]) == True]
      if len(enemys) > 0:
        #THIS IS WHERE YOU DO THINGS TO ENEMY ie DAMAGE or FREEZE or ANYTHING
        return True
    return False
  # Updates relevant game state information
  def on_update(self, delta):
    self.dt = delta
    self.map_machine.update()
    self.map_machine.current.on_update(delta)
    self.update_sprites_collisions_to_walls(delta)
    self.ui.on_update()

    self.is_tongue_collisions_to_enemys()
    if self.is_tongue_collisions_to_walls():
      self.player.stop_bendy_tongue()


