import pygame
import random
import time
import sys

# Initialize Pygame
pygame.init()

# Define constants for screen dimensions and colors
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

# Use default font
FONT = pygame.font.Font(None, 24)  # Default font
BUTTON_FONT = pygame.font.Font(None, 20)

# Set up the display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Sorting Algorithm Selector")

# Function to draw a rounded rectangle
def draw_rounded_rect(surface, color, rect, radius=10):
    pygame.draw.rect(surface, color, rect, border_radius=radius)

# Function to draw a button with hover effect
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

# Sorting Algorithms

def bubble_sort(arr):
    n = len(arr)
    for i in range(n):
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]

def insertion_sort(arr):
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and key < arr[j]:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key

def merge_sort(arr):
    if len(arr) > 1:
        mid = len(arr) // 2
        left_half = arr[:mid]
        right_half = arr[mid:]
        merge_sort(left_half)
        merge_sort(right_half)
        i = j = k = 0
        while i < len(left_half) and j < len(right_half):
            if left_half[i] < right_half[j]:
                arr[k] = left_half[i]
                i += 1
            else:
                arr[k] = right_half[j]
                j += 1
            k += 1
        while i < len(left_half):
            arr[k] = left_half[i]
            i += 1
            k += 1
        while j < len(right_half):
            arr[k] = right_half[j]
            j += 1
            k += 1

def quick_sort(arr):
    if len(arr) <= 1:
        return arr
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    return quick_sort(left) + middle + quick_sort(right)

def radix_sort(arr):
    max_digit = max(arr)
    exp = 1
    while max_digit // exp > 0:
        counting_sort(arr, exp)
        exp *= 10

def counting_sort(arr, exp):
    n = len(arr)
    output = [0] * n
    count = [0] * 10
    for i in arr:
        index = (i // exp) % 10
        count[index] += 1
    for i in range(1, 10):
        count[i] += count[i - 1]
    i = n - 1
    while i >= 0:
        index = (arr[i] // exp) % 10
        output[count[index] - 1] = arr[i]
        count[index] -= 1
        i -= 1
    for i in range(n):
        arr[i] = output[i]

# Checkbox class for algorithm selection
class Checkbox:
    def __init__(self, text, x, y):
        self.text = text
        self.rect = pygame.Rect(x, y, 20, 20)
        self.checked = False
        self.label = FONT.render(text, True, BLACK)
    
    def draw(self, surface):
        pygame.draw.rect(surface, BLACK, self.rect, 2, border_radius=5)
        if self.checked:
            pygame.draw.line(surface, BLACK, (self.rect.x, self.rect.y), (self.rect.x + 20, self.rect.y + 20), 3)
            pygame.draw.line(surface, BLACK, (self.rect.x, self.rect.y + 20), (self.rect.x + 20, self.rect.y), 3)
        surface.blit(self.label, (self.rect.x + 30, self.rect.y))

    def toggle(self):
        self.checked = not self.checked

# Function to draw the UI
def draw_ui(input_box, size_box, generate_box, reset_box, run_box, back_box, checkboxes, text, size_text, color, sorted_arr, results_screen=False, execution_times=None, input_valid=False, validation_message="", active_input=False, active_size=False, blink=False):
    screen.fill(LIGHT_BLUE)
    if not results_screen:
        pygame.draw.rect(screen, WHITE, (40, 40, 920, 130), border_radius=10)
        prompt_surface = FONT.render("Enter numbers (comma-separated):", True, BLACK)
        screen.blit(prompt_surface, (50, 55))
        pygame.draw.rect(screen, WHITE, input_box, border_radius=5)
        pygame.draw.rect(screen, BLACK, input_box, 2, border_radius=5)  # Solid black border
        txt_surface = FONT.render(text, True, BLACK)
        screen.blit(txt_surface, (input_box.x + 10, input_box.y + 5))
        if active_input and blink:  # Draw blinking cursor
            cursor_x = input_box.x + 10 + txt_surface.get_width()
            pygame.draw.line(screen, BLACK, (cursor_x, input_box.y + 5), (cursor_x, input_box.y + 25), 2)

        size_prompt_surface = FONT.render("Enter array size:", True, BLACK)
        screen.blit(size_prompt_surface, (50, 105))
        pygame.draw.rect(screen, WHITE, size_box, border_radius=5)
        pygame.draw.rect(screen, BLACK, size_box, 2, border_radius=5)  # Solid black border
        size_txt_surface = FONT.render(size_text, True, BLACK)
        screen.blit(size_txt_surface, (size_box.x + 10, size_box.y + 5))
        if active_size and blink:  # Draw blinking cursor
            cursor_x = size_box.x + 10 + size_txt_surface.get_width()
            pygame.draw.line(screen, BLACK, (cursor_x, size_box.y + 5), (cursor_x, size_box.y + 25), 2)

        mouse_pos = pygame.mouse.get_pos()
        draw_button(screen, generate_box, "Generate Array", BUTTON_FONT, BLUE, WHITE, generate_box.collidepoint(mouse_pos))
        draw_button(screen, reset_box, "Reset", BUTTON_FONT, RED, WHITE, reset_box.collidepoint(mouse_pos))
        draw_button(screen, run_box, "Run Algorithms & Plot Comparison", BUTTON_FONT, GREEN, WHITE, run_box.collidepoint(mouse_pos))

        for checkbox in checkboxes:
            checkbox.draw(screen)

        sorted_text = FONT.render("Generated Array: " + str(sorted_arr), True, BLACK)
        screen.blit(sorted_text, (50, 350))

        if not input_valid and validation_message:
            validation_surface = FONT.render(validation_message, True, RED)
            screen.blit(validation_surface, (50, 400))
    else:
        pygame.draw.rect(screen, WHITE, (40, 40, 920, 500), border_radius=10)
        y_offset = 50
        for algo, time_taken in execution_times.items():
            result_text = FONT.render(f"{algo}: {time_taken:.2f} microseconds", True, BLACK)
            screen.blit(result_text, (50, y_offset))
            y_offset += 30
        mouse_pos = pygame.mouse.get_pos()
        draw_button(screen, back_box, "Back", BUTTON_FONT, ORANGE, WHITE, back_box.collidepoint(mouse_pos))
    pygame.display.flip()

# Function to validate user input
def validate_input(input_text):
    try:
        numbers = [int(x.strip()) for x in input_text.split(",")]
        return True, numbers
    except ValueError:
        return False, None

# Main function to run the application
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
    checkboxes = [Checkbox("Bubble Sort", 50, 200), Checkbox("Insertion Sort", 50, 230), Checkbox("Merge Sort", 50, 260), Checkbox("Quick Sort", 50, 290), Checkbox("Radix Sort", 50, 320)]
    active_input = False
    active_size = False
    results_screen = False
    execution_times = {}
    input_valid = False
    validation_message = ""
    blink = False
    blink_timer = 0

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
                    if size_text.isdigit():
                        size = int(size_text)
                        arr = [random.randint(1, 100) for _ in range(size)]
                        sorted_arr = arr.copy()
                        input_valid = True
                    else:
                        input_valid, numbers = validate_input(text)
                        if input_valid:
                            arr = numbers
                            sorted_arr = arr.copy()
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
                        execution_times = {}
                        for checkbox in checkboxes:
                            if checkbox.checked:
                                start_time = time.time()
                                if checkbox.text == "Bubble Sort":
                                    bubble_sort(sorted_arr)
                                elif checkbox.text == "Insertion Sort":
                                    insertion_sort(sorted_arr)
                                elif checkbox.text == "Merge Sort":
                                    merge_sort(sorted_arr)
                                elif checkbox.text == "Quick Sort":
                                    sorted_arr = quick_sort(sorted_arr)
                                elif checkbox.text == "Radix Sort":
                                    radix_sort(sorted_arr)
                                end_time = time.time()
                                execution_times[checkbox.text] = (end_time - start_time) * 1_000_000
                        results_screen = True
                    else:
                        validation_message = "Invalid input! Please generate a valid array first."
                elif back_box.collidepoint(event.pos) and results_screen:
                    results_screen = False
                else:
                    active_input = False
                    active_size = False
                for checkbox in checkboxes:
                    if checkbox.rect.collidepoint(event.pos):
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
        blink_timer += 1
        if blink_timer >= 1000:  # Toggle blink every 15 frames (0.25 seconds at 60 FPS)
            blink = not blink
            blink_timer = 0

        draw_ui(input_box, size_box, generate_box, reset_box, run_box, back_box, checkboxes, text, size_text, BLACK, sorted_arr, results_screen, execution_times, input_valid, validation_message, active_input, active_size, blink)
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()