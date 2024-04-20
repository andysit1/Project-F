import pygame as pg
from pygame.math import Vector2
import sys
from random import randrange



#poo
# Initialize pg
pg.init()

# Define constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
WORLD_WIDTH = 1600
WORLD_HEIGHT = 1200
BACKGROUND_COLOR = (255, 255, 255)

#notes
  #this was a dumbass idea

#lessons
  #we need to load the game at the start so we dont have to worry about objects
  #only time we need to blit should be on conditional pop ups
  #got to design the game around preloaded data to reduce the worry about position
  #everything is player located it should else it might be hard to handle
  #good methods to have was
    #screen_to_world()
    #get_world_pos



# Create the world surface
world_surface = pg.Surface((WORLD_WIDTH, WORLD_HEIGHT))

# Create a camera object

# Create a player object

class Player(pg.sprite.Sprite):

    def __init__(self, pos, *groups):
        super().__init__(*groups)
        self.image = pg.Surface((30, 30))
        self.image.fill(pg.Color('dodgerblue1'))
        self.rect = self.image.get_rect(center=pos)
        self.pos = Vector2(pos)
        self.vel = Vector2(0, 0)
        self.speed = 4
        self.attack : bool = False
        self.origin = Vector2(800 // 2, 600 //2)
        self.MAX_DISTANCE = 5

    def handle_event(self, event):
        #Handles player movement
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_d:
                self.vel.x = self.speed
            elif event.key == pg.K_a:
                self.vel.x = -self.speed
            elif event.key == pg.K_w:
                self.vel.y = -self.speed
            elif event.key == pg.K_s:
                self.vel.y = self.speed
            elif event.key == pg.K_SPACE:
                self.attack = True
        elif event.type == pg.KEYUP:
            if event.key == pg.K_d and self.vel.x > 0:
                self.vel.x = 0
            elif event.key == pg.K_a and self.vel.x < 0:
                self.vel.x = 0
            elif event.key == pg.K_w and self.vel.y < 0:
                self.vel.y = 0
            elif event.key == pg.K_s and self.vel.y > 0:
                self.vel.y = 0

        try:
            self.vel = self.vel.normalize() * self.speed
        except:
            pass

    def get_attack_rect(self):
        return pg.rect.Rect(
                self.pos.x,
                self.pos.y,
                self.image.get_width(),
                self.image.get_height()
              )


    def update(self):
    # Move the player.
      self.pos += self.vel
      distance_from_center = self.pos.distance_to(self.origin)

    # Clamp the player within 5 meters radius of the center
      if distance_from_center <= self.MAX_DISTANCE * 10:  # Convert meters to pixels (1 meter = 100 pixels)
        self.rect.center = self.pos
      else:
        self.pos -= self.vel


    # Update player's rectangle position



class Camera:
    def __init__(self, focus):
        #focus/lock on player
        self.focus : Player = focus
        self.view : pg.Surface = pg.display.set_mode((800, 600))
        self.origin = Vector2(800 // 2, 600 //2)
        self.viewP = self.origin.copy()

    def viewpoint(self) -> pg.Surface:
        pass

    def viewpointPosition(self):
        # Calculate the difference between the player and the center of the screen
        heading = self.focus.pos - self.origin
        # Move the camera gradually towards the player
        self.origin += heading * 0.05
        return -self.origin + Vector2(800 // 2, 600 // 2)

    def update(self):
        #calculate the difference between this camera and enity
        heading = self.focus.pos - self.origin
        self.viewP += heading * 0.05
        goto = -self.viewP + self.origin
        # print("update", goto)

all_sprites = pg.sprite.Group()

background_rects = [pg.Rect(randrange(-3000, 3001), randrange(-3000, 3001), 20, 20)
                    for _ in range(500)]


# Create player and camera
player = Player((400, 300), all_sprites)
camera = Camera(player)

# Main game loop
clock = pg.time.Clock()
timer = 0
running = True
while running:
    for event in pg.event.get():
        player.handle_event(event=event)
        if event.type == pg.QUIT:
            running = False

    player.update()
    # Update camera
    camera.update()

    world_surface.fill(BACKGROUND_COLOR)

    for background_rect in background_rects:
        topleft = background_rect.topleft
        pg.draw.rect(world_surface, (200, 50, 70), (topleft, background_rect.size))

    # Draw
    world_surface.blit(player.image, player.rect.topleft)
    if player.attack:
      timer += 0.2
      pg.draw.rect(world_surface, "red", player.get_attack_rect())
      if int(timer) == 2:
          player.attack = False
          timer = 0
    print(camera.viewpointPosition())
    camera.view.blit(world_surface, camera.viewpointPosition())
    # print(camera.origin)
    #draw the camera surface... here...
    pg.display.flip()
    clock.tick(60)

pg.quit()
sys.exit()



#idea
#have surface which represents the world
#this makes it so that we dont have to worry about the offset

#have a camera class which has a reference to the player position
#this then will do all the calculations to the player
  #to prove we can have a player object that moves on it's own and have a camera follow it...