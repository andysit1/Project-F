#!/usr/bin/python3.4
# Setup Python ----------------------------------------------- #
import pygame, sys, random

#DAFLUFFYPOTATO EXAMPLE

# Setup pygame/window ---------------------------------------- #
mainClock = pygame.time.Clock()
from pygame.locals import *
pygame.init()
pygame.display.set_caption('game base')
screen = pygame.display.set_mode((500, 500),0,32)

# a particle is...
# a thing that exists at a location
# typically moves around
# typically changes over time
# and typically disappears after a certain amount of time

# [loc, velocity, timer]
particles = []

# Loop ------------------------------------------------------- #
while True:

    # Background --------------------------------------------- #
    screen.fill((0,0,0))
    mx, my = pygame.mouse.get_pos()
    for particle in particles:
        particle[0][0] += particle[1][0]
        particle[0][1] += particle[1][1]
        particle[2] += 4.3
        particle[3] += 0.3
        # particle[1][1] += 0.05
        screen.fill("black")
        pygame.draw.circle(screen, "red", [int(particle[0][0]), int(particle[0][1])], int(particle[2]) , int(particle[3]))
        if particle[2] >= 70:
            particles.remove(particle)

    # Buttons ------------------------------------------------ #
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN:
            if event.key == K_SPACE:
                particles.append([[mx, my], [0, 0], 20, 1])
            if event.key == K_ESCAPE:
                pygame.quit()
                sys.exit()

    # Update ------------------------------------------------- #
    pygame.display.update()
    mainClock.tick(140)