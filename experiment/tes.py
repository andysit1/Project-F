import pygame as pg

# Initialize Pygame
pg.init()

# Set up the display
screen = pg.display.set_mode((800, 600))
pg.display.set_caption("Half Circle")

# Set colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# Main loop
running = True
while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

    # Clear the screen
    screen.fill(WHITE)

    # Draw half circle
    rect = pg.Rect(100, 100, 200, 200)  # Rectangle to contain the arc
    pg.draw.arc(screen, RED, rect, 0, 3.14, 5)  # Draw half circle (0 to pi radians)

    # Update the display
    pg.display.flip()

# Quit Pygame
pg.quit()
