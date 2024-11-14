import pygame
from game import redraw
from data_fetcher import fetch_map_data
import numpy as np

def interpolate_grid(map_data, scale_factor):
    original_rows = len(map_data)
    original_cols = len(map_data[0])
    new_rows = original_rows * scale_factor
    new_cols = original_cols * scale_factor

    original_grid = np.array(map_data)
    new_grid = np.zeros((new_rows, new_cols))

    # Interpolation logic for resizing
    x_indices = np.linspace(0, original_rows - 1, new_rows)
    y_indices = np.linspace(0, original_cols - 1, new_cols)
    x_floor = np.floor(x_indices).astype(int)
    y_floor = np.floor(y_indices).astype(int)
    x_ceil = np.ceil(x_indices).astype(int)
    y_ceil = np.ceil(y_indices).astype(int)

    x_diff = x_indices - x_floor
    y_diff = y_indices - y_floor

    for i in range(new_rows):
        for j in range(new_cols):
            x1, y1 = x_floor[i], y_floor[j]
            x2, y2 = x_ceil[i], y_ceil[j]

            r1 = (1 - x_diff[i]) * original_grid[x1, y1] + x_diff[i] * original_grid[x2, y1]
            r2 = (1 - x_diff[i]) * original_grid[x1, y2] + x_diff[i] * original_grid[x2, y2]

            new_grid[i, j] = (1 - y_diff[j]) * r1 + y_diff[j] * r2

    # Set values to -1 if they are 0 and not surrounded by land
    for i in range(new_rows):
        for j in range(new_cols):
            if new_grid[i, j] == 0:
                # Check if the current cell is surrounded by water (value 0 or -1)
                neighbors = [
                    (i-1, j), (i+1, j), (i, j-1), (i, j+1),  # Top, Bottom, Left, Right
                    (i-1, j-1), (i-1, j+1), (i+1, j-1), (i+1, j+1)  # Top-Left, Top-Right, Bottom-Left, Bottom-Right
                ]
                surrounded_by_land = False
                for ni, nj in neighbors:
                    if 0 <= ni < new_rows and 0 <= nj < new_cols and new_grid[ni, nj] > 0:
                        surrounded_by_land = True
                        break
                if not surrounded_by_land:
                    new_grid[i, j] = -1

    return new_grid.astype(int).tolist()

def draw_starting_screen(window, window_width, size):
    overlay = pygame.Surface((window_width, size))
    overlay.set_alpha(200)  # Set transparency
    overlay.fill((50, 50, 50))  # Darker color
    window.blit(overlay, (0, 0))

    font = pygame.font.SysFont(None, 72)
    title_text = font.render("Isle Of Heights", True, (255, 255, 255))
    window.blit(title_text, (window_width // 2 - title_text.get_width() // 2, size // 3))

    button_font = pygame.font.SysFont(None, 48)
    button_text = button_font.render("Play Now!", True, (255, 255, 255))
    button_rect = button_text.get_rect(center=(window_width // 2, size // 2))
    pygame.draw.rect(window, (100, 100, 100), button_rect.inflate(20, 10))
    window.blit(button_text, button_rect.topleft)

    return button_rect

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

    map_data = fetch_map_data()
    if not map_data:
        return

    # Interpolate the grid to increase the resolution
    high_res_map_data = interpolate_grid(map_data, scale_factor)
    high_res_rows = rows * scale_factor

    # Print the high resolution map data to verify the values
    for row in high_res_map_data:
        print(row)

    play = True
    clicked_pos = None  # Store the clicked position
    game_started = False
    tries_left = 3 
    while play:
        hover_pos = None
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                play = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if not game_started:
                    if button_rect.collidepoint(mouse_x, mouse_y):
                        game_started = True
                else:
                    clicked_pos = (mouse_x, mouse_y)  # Store the clicked position
                    tries_left -= 1  # Decrease the number of tries left

        # Get the mouse position
        mouse_x, mouse_y = pygame.mouse.get_pos()
        hover_pos = (mouse_x, mouse_y)

        if not game_started:
            button_rect = draw_starting_screen(window, window_width, size)
        else:
            # Redraw the window with the hover effect and clicked position
            redraw(window, hover_pos, size, high_res_rows, high_res_map_data, clicked_pos)

            # Display the number of tries left
            font = pygame.font.SysFont(None, 36)
            # Render the text with a black border
            border_color = (0, 0, 0)
            text_color = (255, 255, 0)
            font = pygame.font.SysFont(None, 36)

            # Render the border by drawing the text multiple times with a slight offset
            border_offsets = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
            for offset in border_offsets:
                border_text = font.render(f'Tries Left: {tries_left}', True, border_color)
                window.blit(border_text, (10 + offset[0], 10 + offset[1]))

            # Render the main text on top
            tries_text = font.render(f'Tries Left: {tries_left}', True, text_color)
            window.blit(tries_text, (10, 10))
            window.blit(tries_text, (10, 10))

            if clicked_pos:
                clicked_pos = None

        pygame.display.update()

    pygame.quit()

if __name__ == "__main__":
    main()