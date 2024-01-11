import pygame
import sys


def process_coordinates(x, y):
    print(x, y)


def screen_reset():
    screen.fill(black)
    pygame.display.flip()
    """Dodac zerowanie matrycy"""


def display_message(message):
    message_font = pygame.font.Font(None, 36)
    message_text = message_font.render(message, True, white)
    screen.blit(message_text, (width // 2 - message_text.get_width() // 2, height - 40))
    pygame.display.flip()


def confirm_number():
    display_message("Twoja liczba została zatwierdzona")


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

# Button variables
button_rect = pygame.Rect(50, height - 70, 100, 50)
clear_button_rect = pygame.Rect(width - 150, height - 70, 100, 50)

# Drawing area rectangle
drawing_area_rect = pygame.Rect(0, 0, width, height - 70)

# Main loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # Sprawdzenie, czy kursor myszy znajduje się w obszarze rysowania
        if drawing_area_rect.collidepoint(pygame.mouse.get_pos()):

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

        else:
            # Sprawdzenie, czy kursor myszy znajduje się poza obszarem
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Sprawdzenie, czy kliknięto w obszarze przycisków
                if button_rect.collidepoint(event.pos):
                    print("Zatwierdź button clicked")
                    confirm_number()
                elif clear_button_rect.collidepoint(event.pos):
                    screen_reset()

        # Rysowanie obszaru rysowania
        pygame.draw.rect(screen, (0, 255, 0), drawing_area_rect, 2)

        # Rysowanie przycisków
        pygame.draw.rect(screen, (0, 128, 255), button_rect)
        pygame.draw.rect(screen, (255, 0, 0), clear_button_rect)
        font = pygame.font.Font(None, 36)
        button_text = font.render("Zatwierdź", True, white)
        clear_button_text = font.render("Wyczyść", True, white)
        screen.blit(button_text, (
            button_rect.centerx - button_text.get_width() // 2,
            button_rect.centery - button_text.get_height() // 2
        ))
        screen.blit(clear_button_text, (
            clear_button_rect.centerx - clear_button_text.get_width() // 2,
            clear_button_rect.centery - clear_button_text.get_height() // 2
        ))

    # Update the display
    pygame.display.flip()
