import pygame
import sys

"""test"""

pygame.init()

# Colors
black = (0, 0, 0)
white = (255, 255, 255)

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

def calculate_grid_data(left_top, side_length, rows, cols):
    cell_width = side_length / cols
    cell_height = side_length / rows

    print(f"Calculated cell_width: {cell_width}, cell_height: {cell_height}")

    grid_info = {
        'cell_width': cell_width,
        'cell_height': cell_height,
        'grid_points': []
    }

    for i in range(rows):
        row_points = []
        for j in range(cols):
            left = left_top[0] + j * cell_width
            top = left_top[1] + i * cell_height
            right = left + cell_width
            bottom = top + cell_height

            print(f"Generating points for cell ({i}, {j}): ({left}, {top}) - ({right}, {bottom})")
            row_points.append(((left, top), (right, bottom)))

        grid_info['grid_points'].append(row_points)

    return grid_info


def generate_grid_points(inner_screen, grid_info, color):
    for row in grid_info['grid_points']:
        for points in row:
            print(f"Drawing rectangle: {points}")
            pygame.draw.rect(inner_screen, color, points, 1)

    pygame.display.flip()

    return grid_info

def draw_internal_grid(surface, left_top, side_length, rows, cols, color, white_points):
    cell_width = side_length // cols
    cell_height = side_length // rows

    for row in range(rows - 1):
        y = left_top[1] + (row + 1) * cell_height
        pygame.draw.line(surface, color, (left_top[0], y), (left_top[0] + side_length, y), 1)

    for col in range(cols - 1):
        x = left_top[0] + (col + 1) * cell_width
        pygame.draw.line(surface, color, (x, left_top[1]), (x, left_top[1] + side_length), 1)

    # Koloruj pola wewnątrz siatki na fioletowo, jeżeli zawierają biały punkt
    for row in range(rows):
        for col in range(cols):
            print(f"Checking cell {row}, {col}")
            cell_rect = pygame.Rect(left_top[0] + col * cell_width, left_top[1] + row * cell_height,
                                    cell_width, cell_height)
            print(f"Cell rect: {cell_rect}")

            if is_white_in_cell(surface, cell_rect):
                print(f"Coloring cell {row}, {col} in purple.")
                pygame.draw.rect(surface, (169, 169, 169), cell_rect)

def is_white_in_cell(surface, cell_rect):
    # Iteracja po wszystkich pikselach wewnątrz komórki
    for y in range(cell_rect.top, cell_rect.bottom):
        for x in range(cell_rect.left, cell_rect.right):
            pixel_color = surface.get_at((x, y))
            # Sprawdzenie, czy kolor piksela jest biały
            if pixel_color == (255, 255, 255, 255):
                return True  # Znaleziono biały piksel w komórce
    return False  # Brak białego piksela w komórce

def confirm_number():
    white_points = []
    for y in range(drawing_area_rect.top, drawing_area_rect.bottom):
        for x in range(drawing_area_rect.left, drawing_area_rect.right):
            pixel_color = screen.get_at((x, y))
            if pixel_color == (255, 255, 255):
                white_points.append((x, y))

    if white_points:
        min_x = min(white_points, key=lambda point: point[0])[0]
        max_x = max(white_points, key=lambda point: point[0])[0]
        min_y = min(white_points, key=lambda point: point[1])[1]
        max_y = max(white_points, key=lambda point: point[1])[1]

        center_x = (min_x + max_x) // 2
        center_y = (min_y + max_y) // 2

        side_length = max(max_x - min_x, max_y - min_y)

        pygame.draw.rect(screen, (0, 0, 255), (min_x, min_y, max_x - min_x, max_y - min_y), 2)
        pygame.draw.circle(screen, (255, 0, 0), (center_x, center_y), 5)
        pygame.draw.rect(screen, (255, 0, 0),
                         (center_x - side_length // 2, center_y - side_length // 2, side_length, side_length), 2)

        grid_rows = 8
        grid_cols = 8
        grid_info = calculate_grid_data((center_x - (side_length / 2), center_y - (side_length / 2)), side_length,
                                        grid_rows, grid_cols)
        #generate_grid_points(screen, grid_info, (169, 169, 169))
        draw_internal_grid(screen, (center_x - (side_length / 2), center_y - (side_length / 2)), side_length, grid_rows,
                           grid_cols, (169, 169, 169), white_points)

        display_message(f"Twoja liczba została zatwierdzona")

    else:
        display_message("Brak punktów do zatwierdzenia")



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