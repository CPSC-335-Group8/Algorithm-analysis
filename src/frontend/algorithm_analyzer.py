import pygame
import random
import time
import sys
import os

# Add backend and graphing directories to Python path
sys.path.append(os.path.abspath("src/backend"))
sys.path.append(os.path.abspath("src/graphing"))

# Import sorting algorithms and utility functions
from bubbleSort import bubble_sort
from mergeSort import merge_sort
from insertionSort import insertion_sort
from quickSort import quick_sort
from radixSort import lsd_radix_sort
from linearSearch import linear_search
from displayGraph import showGraph, getStrings

# Initialize Pygame
pygame.init()

# Screen dimensions and colors
WIDTH, HEIGHT = 1000, 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
DARK_GRAY = (100, 100, 100)
BLUE = (0, 0, 255)
LIGHT_BLUE = (173, 216, 230)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
ORANGE = (255, 165, 0)

# Fonts
FONT = pygame.font.Font(None, 24)
BUTTON_FONT = pygame.font.Font(None, 20)

# Set up display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Sorting Algorithm Selector")

# Render text within a rectangle, wrapping to the next line if necessary.
def draw_text_wrapped(surface, text, font, color, rect, padding=10):
    words = text.split(", ")
    space_width, line_height = font.size(" ")
    x, y = rect.x + padding, rect.y + padding
    max_width = rect.width - 2 * padding

    for i, word in enumerate(words):
        if i < len(words) - 1:
            word += ", "
        word_surface = font.render(word, True, color)
        word_width, _ = word_surface.get_size()

        if x + word_width >= rect.x + max_width:
            x = rect.x + padding
            y += line_height

        surface.blit(word_surface, (x, y))
        x += word_width

# Draw a rectangle with rounded corners.
def draw_rounded_rect(surface, color, rect, radius=10):
    pygame.draw.rect(surface, color, rect, border_radius=radius)

# Draw a button with a hover effect.
def draw_button(surface, rect, text, font, bg_color, text_color, hover=False):
    if hover:
        bg_color = (
            min(bg_color[0] + 20, 255),
            min(bg_color[1] + 20, 255),
            min(bg_color[2] + 20, 255)
        )
    draw_rounded_rect(surface, bg_color, rect)
    text_surface = font.render(text, True, text_color)
    text_rect = text_surface.get_rect(center=rect.center)
    surface.blit(text_surface, text_rect)

# A simple checkbox UI element.
class Checkbox:
    def __init__(self, text, x, y):
        self.text = text
        self.rect = pygame.Rect(x, y, 20, 20)
        self.checked = False
        self.label = FONT.render(text, True, BLACK)

# Draw the checkbox and its label.
    def draw(self, surface):
        pygame.draw.rect(surface, BLACK, self.rect, 2, border_radius=5)
        if self.checked:
            pygame.draw.line(surface, BLACK, (self.rect.x, self.rect.y), (self.rect.x + 20, self.rect.y + 20), 3)
            pygame.draw.line(surface, BLACK, (self.rect.x, self.rect.y + 20), (self.rect.x + 20, self.rect.y), 3)
        surface.blit(self.label, (self.rect.x + 30, self.rect.y))

# Toggle the checkbox state.
    def toggle(self):
        self.checked = not self.checked

# Draw the main user interface.
def draw_ui(input_box, size_box, generate_box, reset_box, run_box, back_box, checkboxes, text, size_text, sorted_arr, results_screen=False, execution_times=None, input_valid=False, validation_message="", active_input=False, active_size=False, blink=False):
    screen.fill(LIGHT_BLUE)
    mouse_pos = pygame.mouse.get_pos()

    if not results_screen:
        pygame.draw.rect(screen, WHITE, (40, 40, 920, 130), border_radius=10)
        screen.blit(FONT.render("Enter numbers (comma-separated):", True, BLACK), (50, 55))
        
        # Input box
        pygame.draw.rect(screen, WHITE, input_box, border_radius=5)
        pygame.draw.rect(screen, BLACK, input_box, 2, border_radius=5)
        formatted_text = text + ("|" if active_input and blink else "")
        txt_surface = FONT.render(formatted_text, True, BLACK)
        screen.blit(txt_surface, (input_box.x + 10, input_box.y + 5))

        # Array size box
        screen.blit(FONT.render("Enter array size:", True, BLACK), (50, 105))
        pygame.draw.rect(screen, WHITE, size_box, border_radius=5)
        pygame.draw.rect(screen, BLACK, size_box, 2, border_radius=5)
        size_txt_surface = FONT.render(size_text + ("|" if active_size and blink else ""), True, BLACK)
        screen.blit(size_txt_surface, (size_box.x + 10, size_box.y + 5))

        # Buttons
        draw_button(screen, generate_box, "Generate Array", BUTTON_FONT, BLUE, WHITE, generate_box.collidepoint(mouse_pos))
        draw_button(screen, reset_box, "Reset", BUTTON_FONT, RED, WHITE, reset_box.collidepoint(mouse_pos))
        draw_button(screen, run_box, "Run Algorithms & Plot Comparison", BUTTON_FONT, GREEN, WHITE, run_box.collidepoint(mouse_pos))

        # Checkboxes
        for checkbox in checkboxes:
            checkbox.draw(screen)

        # Generated array display
        array_label = FONT.render("Generated Array:", True, BLACK)
        screen.blit(array_label, (250, 200))
        array_box = pygame.Rect(250, 220, 600, 180)
        pygame.draw.rect(screen, WHITE, array_box, border_radius=5)
        pygame.draw.rect(screen, BLACK, array_box, 2, border_radius=5)

        if sorted_arr:
            array_text = ", ".join(map(str, sorted_arr))
            draw_text_wrapped(screen, array_text, FONT, BLACK, array_box, padding=10)
        else:
            draw_text_wrapped(screen, "No array generated.", FONT, DARK_GRAY, array_box, padding=10)

        # Validation message
        if validation_message:
            validation_surface = FONT.render(validation_message, True, RED)
            screen.blit(validation_surface, (50, 420))

    else:
        # Results screen
        pygame.draw.rect(screen, WHITE, (40, 40, 920, 500), border_radius=10)
        y_offset = 50
        for algo, time_taken in execution_times.items():
            result_text = FONT.render(f"{algo}: {time_taken:.2f} microseconds", True, BLACK)
            screen.blit(result_text, (50, y_offset))
            y_offset += 30

        draw_button(screen, back_box, "Back", BUTTON_FONT, ORANGE, WHITE, back_box.collidepoint(mouse_pos))

    pygame.display.flip()

# Validate user input to ensure it contains only comma-separated numbers.
def validate_input(input_text):
    try:
        parts = [x.strip() for x in input_text.split(",")]
        if all(part.isdigit() for part in parts):
            numbers = [int(part) for part in parts]
            return True, numbers
        else:
            return False, None
    except ValueError:
        return False, None

# Validate the array size input to ensure it is a positive integer.
def validate_size_input(size_text):
    if size_text.isdigit() and int(size_text) > 0:
        return True, int(size_text)
    return False, None

# Main function to run the application.
def main():
    arr = []
    sorted_arr = []
    input_box = pygame.Rect(350, 50, 400, 32)
    size_box = pygame.Rect(300, 100, 200, 32)
    generate_box = pygame.Rect(50, 150, 150, 40)
    reset_box = pygame.Rect(50, 450, 100, 40)
    run_box = pygame.Rect(160, 450, 300, 40)
    back_box = pygame.Rect(50, 500, 100, 40)
    text = ''
    size_text = ''
    running = True
    checkboxes = [
        Checkbox("Bubble Sort", 50, 200),
        Checkbox("Insertion Sort", 50, 230),
        Checkbox("Merge Sort", 50, 260),
        Checkbox("Quick Sort", 50, 290),
        Checkbox("Radix Sort", 50, 320),
        Checkbox("Linear Search", 50, 350), 
        Checkbox("Select All", 50, 380)  
    ]
    active_input = False
    active_size = False
    results_screen = False
    execution_times = {}
    input_valid = False
    validation_message = ""
    blink = False

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if input_box.collidepoint(event.pos):
                    active_input = True
                    active_size = False
                elif size_box.collidepoint(event.pos):
                    active_size = True
                    active_input = False
                elif generate_box.collidepoint(event.pos):
                    if size_text:
                        size_valid, size = validate_size_input(size_text)
                        if size_valid:
                            arr = [random.randint(1, 100) for _ in range(size)]
                            sorted_arr = arr.copy()
                            input_valid = True
                            validation_message = ""
                        else:
                            validation_message = "Invalid input! Please generate a valid array first."
                    else:
                        input_valid, numbers = validate_input(text)
                        if input_valid:
                            arr = numbers
                            sorted_arr = arr.copy()
                            validation_message = ""
                        else:
                            validation_message = "Invalid input! Please enter numbers separated by commas."
                elif reset_box.collidepoint(event.pos):
                    arr = []
                    sorted_arr = []
                    text = ''
                    size_text = ''
                    input_valid = False
                    validation_message = ""
                    for checkbox in checkboxes:
                        checkbox.checked = False
                elif run_box.collidepoint(event.pos):
                    if input_valid:
                        selected_algorithms = [checkbox for checkbox in checkboxes if checkbox.checked and checkbox.text != "Select All"]
                        if not selected_algorithms:
                            validation_message = "Please select at least one algorithm to run."
                        else:
                            execution_times = {}
                            execution_times["Bubble Sort"] = 0;
                            execution_times["Insertion Sort"] = 0;
                            execution_times["Merge Sort"] = 0;
                            execution_times["Quick Sort"] = 0;
                            execution_times["Radix Sort"] = 0;
                            execution_times["Linear Search"] = 0;
                            for checkbox in selected_algorithms:
                                temp_arr = arr.copy()
                                start_time = time.perf_counter_ns()

                                if checkbox.text == "Bubble Sort":
                                    bubble_sort(temp_arr)
                                elif checkbox.text == "Insertion Sort":
                                    insertion_sort(temp_arr)
                                elif checkbox.text == "Merge Sort":
                                    merge_sort(temp_arr)
                                elif checkbox.text == "Quick Sort":
                                    temp_arr = quick_sort(temp_arr)
                                elif checkbox.text == "Radix Sort":
                                    lsd_radix_sort(temp_arr)
                                elif checkbox.text == "Linear Search":
                                    element = random.choice(temp_arr)
                                    linear_search(temp_arr, element)

                                end_time = time.perf_counter_ns()
                                execution_times[checkbox.text] = int((end_time - start_time) / 1000) #* 1_000_000

                            if execution_times:
                                results_screen = True
                                print(execution_times.values())
                                showGraph(getStrings(list(execution_times.values())))
                    else:
                        validation_message = "Invalid input! Please generate a valid array first."

                elif back_box.collidepoint(event.pos) and results_screen:
                    results_screen = False
                    sorted_arr = arr.copy()
                    validation_message = ""
                else:
                    active_input = False
                    active_size = False
                for checkbox in checkboxes:
                    if checkbox.rect.collidepoint(event.pos):
                        if checkbox.text == "Select All":
                            for cb in checkboxes:
                                if cb != checkbox:
                                    cb.checked = not checkbox.checked
                        else:
                            checkbox.toggle()
            if event.type == pygame.KEYDOWN:
                if active_input:
                    if event.key == pygame.K_BACKSPACE:
                        text = text[:-1]
                    else:
                        text += event.unicode
                elif active_size:
                    if event.key == pygame.K_BACKSPACE:
                        size_text = size_text[:-1]
                    else:
                        size_text += event.unicode

        # Blinking cursor logic
        blink = (pygame.time.get_ticks() // 500) % 2 == 0

        draw_ui(input_box, size_box, generate_box, reset_box, run_box, back_box, checkboxes, text, size_text, sorted_arr, results_screen, execution_times, input_valid, validation_message, active_input, active_size, blink)

if __name__ == "__main__":
    main()