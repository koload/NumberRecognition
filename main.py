import pygame
import sys
import csv
from pygame_gui import UIManager, elements
import numpy as np


# Wczytaj dane z pliku CSV
with open('dates.csv', 'r') as file:
    reader = csv.reader(file)
    next(reader)  # Pomijamy pierwszy wiersz z legendą
    data = list(reader)


class NeuralNetwork:
    # input_size: warstwa 1, hidden_size: warstwa środkowa, out_size: warstwa wyjściowa
    def __init__(self, input_size, hidden_size, output_size):
        # Inicjalizacja wag i obciążeń warstw ukrytej i wyjściowej
        self.weights_input_hidden = np.random.rand(input_size, hidden_size)
        self.weights_hidden_output = np.random.rand(hidden_size, output_size)

        # wektor obciążenia
        self.bias_hidden = np.zeros((1, hidden_size))
        self.bias_output = np.zeros((1, output_size))

    def sigmoid(self, x):
        # Funkcja sigmoidalna do aktywacji neuronów
        return 1 / (1 + np.exp(-x))

    def sigmoid_derivative(self, x):
        # Pochodna funkcji sigmoidalnej
        return x * (1 - x)

    def train(self, inputs, targets, epochs, learning_rate):
        for epoch in range(epochs):
            # Propagacja w przód
            # hidden_layer_input: wartość którą neuron w warstwie środkowej przymuje na wejściu
            hidden_layer_input = np.dot(inputs, self.weights_input_hidden) + self.bias_hidden

            # hidden_layer_output: wartość która neuron w warstwie środkowej przekazuje dalej
            hidden_layer_output = self.sigmoid(hidden_layer_input)

            output_layer_input = np.dot(hidden_layer_output, self.weights_hidden_output) + self.bias_output
            output_layer_output = self.sigmoid(output_layer_input)

            # Obliczenie błędu
            output_error = targets - output_layer_output

            # Propagacja wsteczna
            output_delta = output_error * self.sigmoid_derivative(output_layer_output)
            hidden_error = output_delta.dot(self.weights_hidden_output.T)
            hidden_delta = hidden_error * self.sigmoid_derivative(hidden_layer_output)

            # Aktualizacja wag i obciążeń
            self.weights_hidden_output += hidden_layer_output.T.dot(output_delta) * learning_rate
            self.bias_output += np.sum(output_delta, axis=0, keepdims=True) * learning_rate
            self.weights_input_hidden += inputs.T.dot(hidden_delta) * learning_rate
            self.bias_hidden += np.sum(hidden_delta, axis=0, keepdims=True) * learning_rate

    def predict(self, input):
        # Przewidywanie na podstawie danych wejściowych
        hidden_layer_input = np.dot(input, self.weights_input_hidden) + self.bias_hidden
        hidden_layer_output = self.sigmoid(hidden_layer_input)

        output_layer_input = np.dot(hidden_layer_output, self.weights_hidden_output) + self.bias_output
        output_layer_output = self.sigmoid(output_layer_input)

        return output_layer_output

pygame.init()

trial_number = 0
trial_number_to_tests = 0
user_value = None
input_text = ""
recognized_number = None

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

# Element wprowadzania tekstu
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

# Drawing area rectangle
drawing_area_rect = pygame.Rect(0, 0, width, height - 200)



# Konwertuj dane na numpy array
data_array = np.array(data, dtype=int)

# Pierwsza kolumna zawiera numer próby, druga kolumna zawiera wartość docelową
targets = data_array[:, 1]

# Pozostałe kolumny zawierają informacje o pikselach, użyj ich jako dane treningowe
inputs = data_array[:, 2:]

# Normalizuj dane wejściowe (opcjonalne)
inputs = inputs / 255.0

# Wymiary danych treningowych
num_samples = inputs.shape

# Przygotuj dane docelowe jako macierz o wymiarach (ilość_wierszy_data(num_samples), 10)
target_matrix = np.zeros((len(data), 10))

# Ustal etykiety dla danych
# targets = [sample[0] for sample in data]

# Oznacz odpowiadające próbki w macierzy docelowej
target_matrix[np.arange(len(data)), targets] = 1


# print("\targets", targets)
# print("\nn arrange", np.arange(len(data)))
# print("\ntager_matrix", target_matrix)


# Utwórz instancję sieci neuronowej
input_size = 64  # Liczba pikseli
hidden_size = 32  # Liczba neuronów w warstwie ukrytej
output_size = 10  # Liczba możliwych cyfr od 0 do 9
learning_rate = 0.01
epochs = 10000

# Teraz możesz użyć inputs i target_matrix jako dane do trenowania sieci neuronowej
# Utwórz instancję sieci neuronowej
neural_network = NeuralNetwork(input_size, hidden_size, output_size)

# Trenuj sieć neuronową
neural_network.train(inputs, target_matrix, epochs, learning_rate)


# Funkcja przetwarzająca współrzędne myszy.
def process_coordinates(x, y):
    print(x, y)

# Funkcja resetująca ekran, czyści ekran i odświeża.
def screen_reset():
    screen.fill(black)
    pygame.display.flip()
    """Dodac zerowanie matrycy"""

# Funkcja obliczająca informacje o siatce na podstawie parametrów.
def calculate_grid_data(left_top, side_length, rows, cols):
    cell_width = side_length / cols
    cell_height = side_length / rows

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

            row_points.append(((left, top), (right, bottom)))

        grid_info['grid_points'].append(row_points)

    return grid_info

# Funkcja rysująca siatkę punktów na ekranie.
def generate_grid_points(inner_screen, grid_info, color):
    for row in grid_info['grid_points']:
        for points in row:
            pygame.draw.rect(inner_screen, color, points, 1)

    pygame.display.flip()

    return grid_info

# Funkcja kolorowania wewnętrznych kwadratów (rysująca wewnętrzną siatkę i kolorująca pola z białymi punktami.)
def draw_internal_grid(surface, left_top, side_length, rows, cols, color, white_points):
    # Dodanie +1 żeby ograniczyć przycinanie wyników
    cell_width = (side_length // cols) + 1
    cell_height = (side_length // rows) + 1

    # Lista do przechowywania informacji o każdym kwadracie
    grid_data = []

    global trial_number
    trial_number += 1
    global user_value

    # Dodanie numeru próby i wartości użytkownika do listy
    grid_data.extend([trial_number, user_value])

    for row in range(rows):
        for col in range(cols):
            cell_rect = pygame.Rect(left_top[0] + col * cell_width, left_top[1] + row * cell_height,
                                    cell_width, cell_height)

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

    return grid_data  # Dodaj tę linię, aby funkcja zwracała informacje o zapełnieniu pikseli

# Funkcja sprawdzająca, czy w komórce znajduje się biały punkt.
def is_white_in_cell(surface, cell_rect):
    # Iteracja po wszystkich pikselach wewnątrz komórki
    for y in range(cell_rect.top, cell_rect.bottom):
        for x in range(cell_rect.left, cell_rect.right):
            pixel_color = surface.get_at((x, y))
            # Sprawdzenie, czy kolor piksela jest biały
            if pixel_color == (255, 255, 255, 255):
                return True  # Znaleziono biały piksel w komórce
    return False  # Brak białego piksela w komórce

# Funkcja zapisująca informacje o białych pikselach do pliku CSV.
def save_grid_data(output_file, grid_data):
    with open(output_file, 'a') as file:
        # Konwersja danych do postaci string i zapisanie do pliku
        line = ','.join(map(str, grid_data)) + '\n'
        file.write(line)

def recognize_number(grid_data):
    # Przygotuj dane do przetworzenia przez model
    # input_data = grid_data[2:]  # Pomiń numer próby i wartość użytkownika

    trial_number, user_value, *pixel_data = grid_data
    input_data = pixel_data

    # Przekształć dane na wejście modelu
    input_data = np.array(input_data)

    # Przewiń modele w przód
    prediction = neural_network.predict(input_data)

    # Wyświetl wynik w formie uporządkowanej
    sorted_digits = np.argsort(prediction[0])[::-1]

    print("Przewidywany numer:")
    for i, digit in enumerate(sorted_digits):
        probability = prediction[0][digit]
        print(f"{i + 1}. Cyfra {digit}: {probability}")

    global trial_number_to_tests
    trial_number_to_tests +=1
    print(f"\n\nNumer testu: {trial_number_to_tests} \n\n")

    return prediction

# Funkcja potwierdzająca liczbę na podstawie białych punktów.
def confirm_number():
    white_points = []
    grid_data = []

    for y in range(drawing_area_rect.top, drawing_area_rect.bottom):
        for x in range(drawing_area_rect.left, drawing_area_rect.right):
            pixel_color = screen.get_at((x, y))
            if pixel_color == (255, 255, 255):
                white_points.append((x, y))

    if not white_points:
        message_label.set_text("Brak punktów do zatwierdzenia")
        return None


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
    # Generate_grid_points(screen, grid_info, (169, 169, 169))

    grid_data = draw_internal_grid(screen, ((center_x - (side_length / 2)), (center_y - (side_length / 2))), side_length, grid_rows,
                           grid_cols, (169, 169, 169), white_points)

    message_label.set_text("Twoja liczba została zatwierdzona")

    try:
        prediction = recognize_number(grid_data)
        # return prediction
    except Exception as e:
        print("Error during prediction:", e)
        # return None


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
                # Process_coordinates(mouse_x, mouse_y)

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
                        prediction = confirm_number()

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

        # Rysowanie pola do wpisywania tekstu
        manager.draw_ui(screen)

        # Aktualizuj etykietę z komunikatem
        manager.draw_ui(screen)

    # Update the display
    pygame.display.flip()