import pygame
import sys

# Initialize Pygame
pygame.init()

# Set up the screen dimensions
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Pygame Circle Outline")

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Main game loop
running = True
while running:
    # Check for events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Clear the screen
    screen.fill(BLACK)

    # Draw the outline of a circle (x, y, radius, width)
    pygame.draw.circle(screen, WHITE, (screen_width // 2, screen_height // 2), 50, width=3)

    # Update the display
    pygame.display.flip()

    # Control the frame rate
    pygame.time.Clock().tick(60)

# Quit Pygame
pygame.quit()
sys.exit()
