import pygame
from game import game_loop

def main():
    pygame.init()
    pygame.font.init()

    size = 700
    rows = 30
    scale_factor = 3  # Increase the resolution by a factor of 2
    bar_width = 100  # Width of the color bar
    padding = 20
    text_padding = 50  # Increased padding for text
    window_width = size + bar_width + padding + text_padding + 100  # Increase the window width to accommodate the color bar and text
    window = pygame.display.set_mode((window_width, size))

    game_loop(window, window_width, size, scale_factor, rows)

if __name__ == "__main__":
    main()