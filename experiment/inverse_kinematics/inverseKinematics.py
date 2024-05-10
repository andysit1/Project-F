# Example file showing a basic pygame "game loop"
import pygame

# pygame setup
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True


from typing import Optional


# data representation of a line in pygame. conte
class Segments():
    def __init__(self, point1, point2, head=None):
        self.start : pygame.Vector2 = point1
        self.end : pygame.Vector2 = point2
        self.length = 40
        self.head = head
        self.next = None

    # def set_next_post(self, next_point : pygame.Vector2):
    #     if next_point.distance_to(self.start) > self.length * 2:

    #this part is causing the lag...
    def point_head_towards(self, point : pygame.Vector2):
        try:
            newVector = (point - self.start).normalize()
            newVector = self.end + (newVector * self.length)
            self.start = newVector

        except:
            pass

    def shift_segment(self, point : pygame.Vector2):
        diff = point - self.start
        self.start = pygame.Vector2(round(self.start.x + diff.x), round(self.start.y + diff.y))
        self.end = pygame.Vector2(round(self.end.x + diff.x), round(self.end.y + diff.y))

    def uppdate(self):
        if self.start.distance_to(pygame.mouse.get_pos()) > self.length * 2:
            self.point_head_towards(pygame.mouse.get_pos())
            self.shift_segment(pygame.mouse.get_pos())

    def update_position(self, location : pygame.Vector2):
        if self.start.distance_to(location):
            self.point_head_towards(location)
            self.shift_segment(location)

    def draw(self, surface):
        pygame.draw.line(surface, "white", self.start, self.end, 5)


class SegmentsConnector():
    def __init__(self):
        self.segment_list : list[Segments] = []
        self.head = None

    def add_head(self, head : Segments):
        self.head = head

    def add(self, seg : Segments):
        self.segment_list.append(seg)

    def update(self):
        prev : Segments = None

        for seg in self.segment_list:
            if prev:
                seg.point_head_towards(prev.end)
                if seg.start != prev.end:
                    seg.shift_segment(prev.end)

            prev = seg

    def draw(self, surface):
        for seg in self.segment_list:
            if seg.head:
                pygame.draw.line(surface, "red", seg.start, seg.end, 10)
            else:
                pygame.draw.line(surface, "white", seg.start, seg.end, 10)


# if __name__ == "__main__":
#     main()


seg_surf = pygame.Surface([100, 100])
seg_surf.fill("black")
pygame.draw.line(seg_surf, "White", (0, 50), (100, 50))


print("Testing Segment Proto")
point1 = pygame.Vector2(100, 100)
point2 = pygame.Vector2(100, 150)
point3 = pygame.Vector2(150, 150)
point4 = pygame.Vector2(160, 180)



seg1 = Segments(point1, point2, True)
seg2 = Segments(point2, point3)
seg3 = Segments(point3, point4)

connector = SegmentsConnector()
connector.add(seg1)
connector.add(seg2)
connector.add(seg3)

connector.add_head(seg1)

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window

    seg1.update_position(pygame.mouse.get_pos())

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # if event.type == pygame.KEYDOWN:
        #     if event.key == pygame.K_DOWN:
        #         seg1.shift_segment(pygame.mouse.get_pos())
    # seg1.start =  pygame.mouse.get_pos()

    connector.update()




    # fill the screen with a color to wipe away anything from last frame
    screen.fill("purple")
    connector.draw(screen)
    # screen.blit(seg_surf, (0,0))


    # RENDER YOUR GAME HERE

    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(60)  # limits FPS to 60

pygame.quit()