import pygame
import sys
from pygame_gui import UIManager, elements

#Pamiętaj o:    pip install pygame_gui

pygame.init()

trial_number = 0
user_value = None
input_text = ""

# Colors
black = (0, 0, 0)
white = (255, 255, 255)

# Display
width, height = 800, 800
icon = pygame.image.load('Number_sign.png')

screen = pygame.display.set_mode((width, height))
screen.fill(black)
pygame.display.set_caption("Number Recognition")
pygame.display.set_icon(icon)

# Inicjalizacja pygame_gui
manager = UIManager((width, height))

# Przykładowy element wprowadzania tekstu
text_input_rect = pygame.Rect((75, height - 150), (200, 35))
text_input = elements.UITextEntryLine(relative_rect=text_input_rect, manager=manager)

# Przycisk "Zatwierdź"
confirm_button_rect = pygame.Rect((75, height - 100), (100, 50))
confirm_button = elements.UIButton(relative_rect=confirm_button_rect, text='Zatwierdź', manager=manager)

# Przycisk "Wyczyść"
clear_button_rect = pygame.Rect((width - 175, height - 100), (100, 50))
clear_button = elements.UIButton(relative_rect=clear_button_rect, text='Wyczysc', manager=manager)

# Label do wyświetlania komunikatów
message_label_rect = pygame.Rect((width - 350, height - 150), (400, 50))
message_label = elements.UILabel(relative_rect=message_label_rect, text='', manager=manager)


# Drawing variables
drawing = False
last_pos = None

# Button variables
#button_rect = pygame.Rect(50, height - 70, 100, 50)
#clear_button_rect = pygame.Rect(width - 150, height - 70, 100, 50)

# Drawing area rectangle
drawing_area_rect = pygame.Rect(0, 0, width, height - 200)




#Funkcja przetwarzająca współrzędne myszy.
def process_coordinates(x, y):
    print(x, y)

#Funkcja resetująca ekran, czyści ekran i odświeża.
def screen_reset():
    screen.fill(black)
    pygame.display.flip()
    """Dodac zerowanie matrycy"""

#Funkcja wyświetlająca komunikat na dole ekranu.
def display_message(message):
    message_font = pygame.font.Font(None, 36)
    message_text = message_font.render(message, True, white)
    screen.blit(message_text, (width // 2 - message_text.get_width() // 2, height - 40))
    pygame.display.flip()

#Funkcja obliczająca informacje o siatce na podstawie parametrów.
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

#Funkcja rysująca siatkę punktów na ekranie.
def generate_grid_points(inner_screen, grid_info, color):
    for row in grid_info['grid_points']:
        for points in row:
            print(f"Drawing rectangle: {points}")
            pygame.draw.rect(inner_screen, color, points, 1)

    pygame.display.flip()

    return grid_info

#Funkcja kolorowania wewnętrznych kwadratów (rysująca wewnętrzną siatkę i kolorująca pola z białymi punktami.)
def draw_internal_grid(surface, left_top, side_length, rows, cols, color, white_points):
    cell_width = side_length // cols
    cell_height = side_length // rows

    # Lista do przechowywania informacji o każdym kwadracie
    grid_data = []

    global trial_number
    trial_number += 1
    global user_value

    # Dodanie numeru próby i wartości użytkownika do listy
    grid_data.extend([trial_number, user_value])

    for row in range(rows):
        for col in range(cols):
            print(f"Checking cell {row}, {col}")
            cell_rect = pygame.Rect(left_top[0] + col * cell_width, left_top[1] + row * cell_height,
                                    cell_width, cell_height)
            print(f"Cell rect: {cell_rect}")

            # Sprawdzenie, czy w komórce znajdują się białe piksele
            is_white = is_white_in_cell(surface, cell_rect)

            # Dodanie informacji o białych pikselach do listy
            grid_data.append(1 if is_white else 0)

            # Pomalowanie kwadratu na szaro, jeśli zawiera białe piksele
            if is_white:
                pygame.draw.rect(surface, (169, 169, 169), cell_rect)

    # Zapisanie informacji o białych pikselach do pliku
    save_grid_data('dates.csv', grid_data)

    # Aktualizacja ekranu
    pygame.display.flip()

#Funkcja sprawdzająca, czy w komórce znajduje się biały punkt.
def is_white_in_cell(surface, cell_rect):
    # Iteracja po wszystkich pikselach wewnątrz komórki
    for y in range(cell_rect.top, cell_rect.bottom):
        for x in range(cell_rect.left, cell_rect.right):
            pixel_color = surface.get_at((x, y))
            # Sprawdzenie, czy kolor piksela jest biały
            if pixel_color == (255, 255, 255, 255):
                return True  # Znaleziono biały piksel w komórce
    return False  # Brak białego piksela w komórce

#Funkcja zapisująca informacje o białych pikselach do pliku CSV.
def save_grid_data(output_file, grid_data):
    with open(output_file, 'a') as file:
        # Konwersja danych do postaci string i zapisanie do pliku
        line = ','.join(map(str, grid_data)) + '\n'
        file.write(line)

#Funkcja potwierdzająca liczbę na podstawie białych punktów.
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

        #display_message(f"Twoja liczba została zatwierdzona")
        message_label.set_text("Twoja liczba została zatwierdzona")

    else:
        #display_message("Brak punktów do zatwierdzenia")
        message_label.set_text("Brak punktów do zatwierdzenia")


# Main loop
while True:
    time_delta = pygame.time.Clock().tick(60) / 1000.0  # Obliczenie delta czasu tylko raz

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # Pobierz aktualne zdarzenia
        events = pygame.event.get()

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
                if confirm_button_rect.collidepoint(event.pos):
                    input_text = text_input.get_text().strip()

                    if input_text:
                        user_value = int(input_text)
                        print(f"Wprowadzony numer: {user_value}")
                        confirm_number()
                    else:
                        message_label.set_text("Pole tekstowe jest puste. Wprowadź numer.")

                elif clear_button_rect.collidepoint(event.pos):
                    screen_reset()

            # Obsługa zdarzeń klawiatury dla pygame_gui
            manager.process_events(event)

        # Aktualizacja pygame_gui
        manager.update(time_delta)

        # Rysowanie obszaru rysowania
        pygame.draw.rect(screen, (0, 255, 0), drawing_area_rect, 2)

        # Rysowanie przycisków
        #pygame.draw.rect(screen, (0, 128, 255), button_rect)
        #pygame.draw.rect(screen, (255, 0, 0), clear_button_rect)
        #font = pygame.font.Font(None, 36)
        #button_text = font.render("Zatwierdź", True, white)
        #clear_button_text = font.render("Wyczyść", True, white)
        #screen.blit(button_text, (
        #    button_rect.centerx - button_text.get_width() // 2,
        #    button_rect.centery - button_text.get_height() // 2
        #))
        #screen.blit(clear_button_text, (
        #    clear_button_rect.centerx - clear_button_text.get_width() // 2,
        #    clear_button_rect.centery - clear_button_text.get_height() // 2
        #))

        # Rysowanie pola do wpisywania tekstu
        manager.draw_ui(screen)

        # Aktualizuj etykietę z komunikatem
        manager.draw_ui(screen)

    # Update the display
    pygame.display.flip()
