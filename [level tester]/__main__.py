import pygame
import pytmx
import os

# Function to load Tiled map
def load_map(map_file):
    tm = pytmx.load_pygame(map_file)
    return tm

# Function to draw Tiled map
def draw_map(screen, tm):
    # Draw each layer in the map
    for layer in tm.visible_layers:
        if isinstance(layer, pytmx.TiledTileLayer):
            for x, y, gid in layer:
                tile = tm.get_tile_image_by_gid(gid)
                if tile:
                    screen.blit(tile, (x * tm.tilewidth, y * tm.tileheight))

def main():
    # Initialize pygame
    pygame.init()

    # Set the dimensions of the window
    screen_width = 800
    screen_height = 600

    parent_dir = os.path.dirname(os.path.dirname(__file__))
    uitImagePath = os.path.join(parent_dir, "[level tester]", "trial_blue", "blue_trial.tmx")


    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Tiled Map Test")

    tm = load_map(uitImagePath)

    # Main loop
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Clear the screen
        screen.fill((0, 0, 0))

        # Draw the map
        draw_map(screen, tm)

        # Update the display
        pygame.display.flip()

    # Quit pygame
    pygame.quit()

if __name__ == "__main__":
    main()