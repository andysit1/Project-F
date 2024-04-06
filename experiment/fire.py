#                 Pygame VFX                #
#             MIT - Kadir Aksoy             #
#   https://github.com/kadir014/pygame-vfx  #


import platform
from random import randint, choice
from math import atan2, cos, sin, sqrt
import pygame


from PIL import Image, ImageFilter
import pygame


#REFERENCE
#https://www.youtube.com/watch?v=QUpUWL7xw5g
# https://github.com/kadir014/pygame-vfx

#rawrr i understand this :)








# Optimized blurring algorithm by The New St. Paul aka MintFan
#pretty sure this might be useful as we continue...
def blur(canvas, pos, size, radius=10, alpha=255, resolution=40):
    resolution = resolution #percentage of pixels to use for blur
    s = pygame.Surface(size)
    s.blit(canvas, (0, 0), (pos[0], pos[1], size[0], size[1]))
    s = pygame.transform.rotozoom(s, 0, (resolution / 100.0) * 1)
    size2 = s.get_size()
    rad = radius
    b = pygame.image.tostring(s, "RGBA", False)
    b = Image.frombytes("RGBA", size2, b)
    b = b.filter(ImageFilter.GaussianBlur(radius=int(rad)))
    b = pygame.image.frombuffer(b.tobytes(), b.size, b.mode).convert()
    b.set_alpha(alpha)
    b = pygame.transform.rotozoom(b, 0, (100.0 / resolution) * 1)
    canvas.blit(b, pos)


### Initialize window

WINDOW_WIDTH, WINDOW_HEIGHT = 1280, 720

pygame.init()
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption(f"Pygame VFX Playground   •   Python {platform.python_version()}  Pygame {pygame.version.ver}  SDL {'.'.join([str(v) for v in pygame.get_sdl_version()])}")
clock = pygame.time.Clock()
running = True

res = 4
bsurf = pygame.Surface((1280//res, 720//res), pygame.SRCALPHA).convert_alpha()

hint = pygame.Surface((380, 90), pygame.SRCALPHA).convert_alpha()

# you can change the palette
palette = ((255, 255, 0),
            (255, 173, 51),
            (247, 117, 33),
            (191, 74, 46),
            (115, 61, 56),
            (61, 38, 48))[::-1]

class Slider:
    def __init__(self, x, y, w, h, min, max):
        self.x, self.y, self.w, self.h = x, y, w, h
        self.min, self.max = min, max
        self.val = self.min
        self.valx = self.x

    def set_val(self, val):
        self.val = val
        self.valx = self.x + self.w*(self.val/(self.max-self.min))

    def update(self, mx, my, mp):
        if mp and ms:
            if pygame.Rect(self.x, self.y, self.w, self.h).collidepoint((mx, my)):
                   self.val = ((mx - self.x)/self.w)*(self.max-self.min)+self.min
                   self.valx = mx

sliders = list()

sliders.append(Slider(11, 106+21, 150, 10, 0.25, 15))
sliders.append(Slider(11, 150+21, 150, 10, 1, 10))
sliders.append(Slider(11, 194+21, 150, 10, 0, 2))
sliders.append(Slider(11, 238+21, 150, 10, 0, 3))
sliders.append(Slider(11, 282+21, 150, 10, -2, 2))

sliders[0].set_val(2.9)
sliders[1].set_val(3)
sliders[2].set_val(1.25)
sliders[3].set_val(1.0)
sliders[4].set_val(0)

uisurf = pygame.Surface((180, 720)).convert()
uisurf.set_alpha(85)



### Particle class

class Particle:
    def __init__(self, x, y):
        self.x, self.y = x, y
        self.maxlife = randint(13 + int(sliders[0].val*5), 27 + int(sliders[0].val*10))
        self.life = self.maxlife
        self.dir = choice((-2, -1, 1, 2))
        self.sin = randint(-10, 10)/7
        self.sinr = randint(5, 10)
        self.r = randint(0,2)

        self.ox = randint(-1, 1)
        self.oy = randint(-1, 1)

particles = list()
dead = list()



j = 0
#origin of click
ox, oy = pygame.mouse.get_pos()
fs = False
fa = 255
ms = False



while running:
    j += 1
    if j > 360: j = 0
    clock.tick(60)

    mx, my = pygame.mouse.get_pos()
    dist = sqrt((mx-ox)**2+(my-oy)**2)


    #left click
    mp = pygame.mouse.get_pressed()[0]


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if mx < 180: ms = True
            else: ms = False

    #ms is true when in slider bar
    if not ms:
        if mp: fs = True
        a = atan2(my-oy, mx-ox)
        for d in range(0, int(dist), 10):
            _x = mx+cos(a)*d
            _y = my+sin(a)*d
            if mp:
                for _ in range(round(sliders[1].val)): particles.append(Particle(_x//res, _y//res))
        else:
            if mp:
                for _ in range(round(sliders[1].val)): particles.append(Particle(mx//res, my//res))


    window.fill((24, 20, 36))
    bsurf.fill((0, 0, 0, 0))

    if fa > 0:
        window.blit(hint, (530, 310))

    if fs:
        fa -= 5
        if fa < 0: fs = False
        else: hint.set_alpha(fa)


    #draws the literal dot at curor of the inital fire...
    #good for physical touches
    if mp and not ms:
        pygame.draw.circle(bsurf, palette[5], (mx//res, my//res-2), 2, 0)

    #um this is confusing...
    for p in particles:
        p.life -= 1
        if p.life == 0: dead.append(p); continue

        i = int((p.life/p.maxlife)*6)

        p.y -= sliders[2].val
        p.x += ((p.sin * sin(j/(p.sinr)))/2)*sliders[3].val + sliders[4].val

        if not randint(0, 5): p.r += 0.88

        x, y = p.x, p.y

        x += p.ox*(5-i)
        y += p.oy*(5-i)

        alpha = 255

        #if life of particle is less than quarter than set the transparency of the particle
        if p.life < p.maxlife/4:
            alpha = int((p.life/p.maxlife)*255)


        pygame.draw.circle(bsurf, palette[i] + (alpha,), (x, y), p.r, 0)

        if i == 0:
            #what does this even do...
            pygame.draw.circle(bsurf, (0, 0, 0, 0), (x+randint(-1, 1), y-4), p.r*(((p.maxlife-p.life)/p.maxlife)/0.88), 0)
        else:
            #this draws the darker insides inside the circle,   x+randit is used to make it look more real by randomix left or right of the center circle, size of it should be a half smaller than the original size...
            pygame.draw.circle(bsurf, palette[i-1] + (alpha,), (x+randint(-1, 1), y-3), p.r/1.5, 0)


    window.blit(pygame.transform.scale(bsurf, (1280, 720)), (0, 0))


    #IDK IF THIS IS DOING ANYTHING
    blur(window, (0, 0), (180, 720))

    window.blit(uisurf, (0, 0))

    pygame.draw.line(window, (251, 250, 252), (11, 60), (169, 60), 1)

    for slider in sliders:
        slider.update(mx, my, mp)
        pygame.draw.rect(window, (255,255,255), (slider.x+slider.h/2, slider.y, slider.w-slider.h, slider.h), 0)
        pygame.draw.circle(window, (255,255,255), (slider.x+slider.h/2, slider.y+slider.h/2), slider.h/2)
        pygame.draw.circle(window, (255,255,255), (slider.x+slider.w-slider.h/2, slider.y+slider.h/2), slider.h/2)
        pygame.draw.circle(window, (255, 160, 0), (slider.valx, slider.y+slider.h/2), slider.h/2)

    pygame.draw.rect(window, (251, 250, 252), (105, 76, 62, 18), 0)

    for i, c in enumerate(palette):
        pygame.draw.rect(window, c, (106+(i*10), 77, 10, 16), 0)

    for p in dead:
        particles.remove(p)
    dead.clear()

    pygame.display.flip()
    ox, oy = mx, my

pygame.quit()