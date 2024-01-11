import pygame
import sys

"""test 11.1"""

def process_coordinates(x, y):
    print(x, y)


def screen_reset():
    screen.fill(black)
    pygame.display.flip()
    """Dodac zerowanie matrycy"""


pygame.init()

# Colors
black = (0, 0, 0)
white = (255, 255, 255)


# Display
width, height = 800, 600
icon = pygame.image.load('Number_sign.png')

screen = pygame.display.set_mode((width, height))
screen.fill(black)
pygame.display.set_caption("Number Recognition")
pygame.display.set_icon(icon)

# Drawing variables
drawing = False
last_pos = None

# Main loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            drawing = True
            last_pos = pygame.mouse.get_pos()

        if event.type == pygame.MOUSEBUTTONUP:
            drawing = False
            last_pos = None

        if event.type == pygame.MOUSEMOTION and drawing:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            process_coordinates(mouse_x, mouse_y)

            current_pos = pygame.mouse.get_pos()
            pygame.draw.line(screen, white, last_pos, current_pos, 2)
            last_pos = current_pos

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                screen_reset()

    # Update the display
    pygame.display.flip()


