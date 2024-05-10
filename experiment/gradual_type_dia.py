import pygame
from sys import exit
pygame.init()

WIN = pygame.display.set_mode((1000,600))
clock = pygame.time.Clock()

textbox_surf = pygame.Surface((700,200), pygame.SRCALPHA)
textbox_rect = textbox_surf.get_rect(topleft=(150,200))
border_rect = textbox_surf.get_rect(topleft=(0, 0))

FONT = pygame.font.SysFont(None, 24, 0)
s = "This is just an example text to use with gradual typing."
show_textbox = False
typing = False

test_text = FONT.render(s, 1, 'White')
text_rect = test_text.get_rect(topleft=(20, 90))

def gradual_typing(txt):
    global typing
    rendering = ''

    WIN.blit(textbox_surf, textbox_rect)
    pygame.display.update()

    for char in txt:
        pygame.time.delay(35) #use dt instead...
        pygame.event.clear()

        rendering = rendering + char
        rendered_text = FONT.render(rendering, 1, 'White')
        text_rect = rendered_text.get_rect(topleft=(20, 90))

        WIN.fill('Grey')
        textbox_surf.fill((0, 0, 255, 100))
        pygame.draw.rect(textbox_surf, "Black", border_rect, 6)
        textbox_surf.blit(rendered_text, text_rect)
        WIN.blit(textbox_surf, textbox_rect)

        pygame.display.update()

    typing = False


while True:
    clock.tick(30)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                show_textbox = True
                typing = True

    WIN.fill('Grey')

    if show_textbox:

        if typing:
            gradual_typing(s)

    WIN.blit(textbox_surf, textbox_rect)
    pygame.display.update()