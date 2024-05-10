# Example file showing a basic pygame "game loop"
import pygame
from random import randint, uniform

# pygame setup
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True

MAX_FORCE = 10
vec = pygame.math.Vector2
frect = pygame.rect.FRect
# Mob properties
MOB_SIZE = 32
MAX_SPEED = 4
MAX_FORCE = 0.4
RAND_TARGET_TIME = 500
WANDER_RING_DISTANCE = 150
WANDER_RING_RADIUS = 50
WANDER_TYPE = 2


class EntityMovementAI():
    def __init__(self):
        self.pos = vec(100, 100)
        self.vel = vec(MAX_SPEED, 0).rotate(uniform(0, 360))
        self.acc = vec(0, 0)
        self.head : frect = None
        self.collision_zone : frect = frect(50, 50, 1120, 730)

    def seek(self, target):
        self.desired = (target - self.pos).normalize() * MAX_SPEED
        steer = (self.desired - self.vel)
        if steer.length() > MAX_FORCE:
            steer.scale_to_length(MAX_FORCE)
        return steer

    def wander_improved(self):
        future = self.pos + self.vel.normalize() * WANDER_RING_DISTANCE
        #add a bias to make the AI go towards the center
        target = future + vec(WANDER_RING_RADIUS, 0).rotate(uniform(0, 360))
        self.displacement = target
        return self.seek(target)

    def update(self):
        if WANDER_TYPE == 1:
            self.acc = self.wander()
        else:
            if not self.head.colliderect(self.collision_zone):
                self.acc = self.seek(vec(self.collision_zone.center[0], self.collision_zone.center[1]))
            else:
                self.acc = self.wander_improved()


        self.vel += self.acc
        if self.vel.length() > MAX_SPEED:
            self.vel.scale_to_length(MAX_SPEED)
        self.pos += self.vel


class SoftBody():
    def __init__(self):
        self.body_length : int = 8
        self.part_offset : int = 20
        self.body_parts : list[pygame.Vector2] = []
        self.head : frect = frect(0, 0, 25, 25)
        self.pos = None

    def add_body(self, part : pygame.Vector2):
        if len(self.body_parts) == 0:
            self.body_parts.append(part)
        else:
            if not self.add_conditions_ai(part):
                return

            if len(self.body_parts) > self.body_length:
                self.body_parts.pop()
                self.body_parts.insert(0, part)
            else:
                self.body_parts.insert(0, part)

    @property
    def body_part_length(self):
        return len(self.body_parts)

    def to_vector_2d(self, pos):
        if isinstance(pos, vec):
            return pos

        return pygame.Vector2(pos[0], pos[1])

    def add_conditions(self) -> bool:
        if self.body_part_length > 0:
          if (self.body_parts[0] -  self.to_vector_2d(pygame.mouse.get_pos())).magnitude() > self.part_offset:
              return True

    def add_conditions_ai(self, location) -> bool:
        if self.body_part_length > 0:
            if (self.body_parts[0] - self.to_vector_2d(location)).magnitude() > self.part_offset:
                return True

    def update(self):
        if not self.pos:
            self.add_body(part=pygame.mouse.get_pos())
            self.head.center = self.body_parts[0]

        if self.pos:
            self.add_body(part=self.pos.copy())

        self.head.center = self.body_parts[0]


    def draw(self, surface):
        size = 13
        prev = None
        for part in self.body_parts:
            size -= 1.2
            if prev:
                pygame.draw.line(screen, "black", prev, part, 1)
            pygame.draw.circle(surface, "white", part, radius=size, width=2)
            prev = part

        pygame.draw.rect(surface, "blue", self.head)

entity1 = SoftBody()

entity2 = SoftBody()
AI1 = EntityMovementAI()


AI1.head = entity2.head

entity2.pos = AI1.pos


entities = []
ai = []

for i in range(5):
    bodyobj = SoftBody()
    aiobj = EntityMovementAI()



    aiobj.head = bodyobj.head
    bodyobj.pos = aiobj.pos

    entities.append(bodyobj)
    ai.append(aiobj)


def update_ai():
    for i in ai:
        i.update()

    for i in entities:
        i.update()

def draw_entities(surf):
    for i in entities:
        i.draw(surf)

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False


    update_ai()

    entity1.update()

    screen.fill("purple")

    #player controled
    entity1.draw(screen)

    #AI controlled
    draw_entities(screen)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()