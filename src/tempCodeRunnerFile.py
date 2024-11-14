import pygame
from game import redraw
from data_fetcher import fetch_map_data

def main():
    size = 700
    rows = 30
    window = pygame.display.set_mode((size, size))

    map_data = fetch_map_data()
    if not map_data:
        return

    play = True
    while play:
        hover_pos = None
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                play = False

        # Get the mouse position
        mouse_x, mouse_y = pygame.mouse.get_pos()
        hover_pos = (mouse_x, mouse_y)

        # Redraw the window with the hover effect
        redraw(window, hover_pos, size, rows, map_data)

    pygame.quit()

if __name__ == "__main__":
    main()