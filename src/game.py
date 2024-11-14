import pygame
from grid import draw_grid, highlight_cell, draw_color_bar, get_color_steps
from data_fetcher import fetch_map_data
import numpy as np
from collections import deque
import time

def time_trial_mode(window, window_width, size, scale_factor, rows):
    def reset_time_trial():
        return reset_game(scale_factor, rows, window, size)

    # Initialize game variables
    map_data, high_res_map_data, high_res_rows, clicked_pos, game_started, tries_left, islands, island_averages, max_avg_height = reset_time_trial()

    play = True
    message = None
    all_island_edges = []  # List to store edges of all scanned islands
    score = 0
    start_time = time.time()
    time_limit = 60  # 1 minute time limit
    paused_time = 0  # Time spent in paused state

    while play:
        hover_pos = None
        current_time = time.time()
        elapsed_time = current_time - start_time - paused_time
        remaining_time = max(0, time_limit - elapsed_time)

        if remaining_time <= 0:
            play = False
            draw_time_trial_summary(window, window_width, size, score, scale_factor, rows)
            break

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                play = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                clicked_pos = (mouse_x, mouse_y)  # Store the clicked position
                distanceBtwRows = size / high_res_rows  # Use float division to get precise distance
                cell_x = int(clicked_pos[0] // distanceBtwRows)
                cell_y = int(clicked_pos[1] // distanceBtwRows)
                clicked_island_avg_height = None
                for island, avg_height in zip(islands, island_averages):
                    if (cell_x, cell_y) in island:
                        clicked_island_avg_height = avg_height
                        # Pause the timer
                        pause_start_time = time.time()
                        # Visualize the flood fill process for the clicked island
                        flood_fill(high_res_map_data, cell_x, cell_y, set(), window, size, high_res_rows, "Calculating...")
                        pause_end_time = time.time()
                        paused_time += pause_end_time - pause_start_time  # Add the paused duration to paused_time
                        island_edges = get_island_edges(island, high_res_map_data)
                        all_island_edges.append(island_edges)  # Add the edges to the list of all scanned islands
                        if avg_height == max_avg_height:
                            score += 1
                            message = "Correct! Score: {}".format(score)
                            # Generate a new map for the next round
                            map_data, high_res_map_data, high_res_rows, clicked_pos, game_started, tries_left, islands, island_averages, max_avg_height = reset_time_trial()
                            all_island_edges = []  # Clear the edges of the previously guessed islands
                        else:
                            message = "Wrong guess. Try again."
                        break
                print(f'Max average height: {max_avg_height}')
                print(f'Clicked island average height: {clicked_island_avg_height}')
                print(f'Clicked position: ({cell_x}, {cell_y})')

        # Get the mouse position
        mouse_x, mouse_y = pygame.mouse.get_pos()
        hover_pos = (mouse_x, mouse_y)

        # Redraw the window with the hover effect and clicked position
        redraw(window, hover_pos, size, high_res_rows, high_res_map_data, clicked_pos, message, all_island_edges)

        # Display the remaining time
        font = pygame.font.SysFont(None, 36)
        time_text = font.render(f'Time Left: {int(remaining_time)}s', True, (255, 255, 255))
        window.blit(time_text, (10, 50))

        pygame.display.update()

    pygame.quit()

def precision_mode(window, window_width, size, scale_factor, rows):
    def reset_precision_mode(tries_left):
        map_data, high_res_map_data, high_res_rows, clicked_pos, game_started, _, islands, island_averages, max_avg_height = reset_game(scale_factor, rows, window, size)
        return map_data, high_res_map_data, high_res_rows, clicked_pos, game_started, tries_left, islands, island_averages, max_avg_height

    # Initialize game variables
    tries_left = 10  # Set the initial number of tries to 10
    map_data, high_res_map_data, high_res_rows, clicked_pos, game_started, tries_left, islands, island_averages, max_avg_height = reset_precision_mode(tries_left)

    play = True
    message = None
    all_island_edges = []  # List to store edges of all scanned islands
    correct_guesses = 0

    while play:
        hover_pos = None

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                play = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                clicked_pos = (mouse_x, mouse_y)  # Store the clicked position
                distanceBtwRows = size / high_res_rows  # Use float division to get precise distance
                cell_x = int(clicked_pos[0] // distanceBtwRows)
                cell_y = int(clicked_pos[1] // distanceBtwRows)
                clicked_island_avg_height = None
                for island, avg_height in zip(islands, island_averages):
                    if (cell_x, cell_y) in island:
                        clicked_island_avg_height = avg_height
                        # Visualize the flood fill process for the clicked island
                        flood_fill(high_res_map_data, cell_x, cell_y, set(), window, size, high_res_rows, "Calculating...")
                        island_edges = get_island_edges(island, high_res_map_data)
                        all_island_edges.append(island_edges)  # Add the edges to the list of all scanned islands
                        if avg_height == max_avg_height:
                            correct_guesses += 1
                            message = "Correct! Guessed: {}".format(correct_guesses)
                            # Generate a new map for the next round, keeping the current number of tries left
                            map_data, high_res_map_data, high_res_rows, clicked_pos, game_started, tries_left, islands, island_averages, max_avg_height = reset_precision_mode(tries_left)
                            all_island_edges = []  # Clear the edges of the previously guessed islands
                        else:
                            tries_left -= 1
                            message = "Wrong guess. Tries left: {}".format(tries_left)
                            # Highlight the missed island for a moment
                            pygame.time.delay(1000)
                        break
                print(f'Max average height: {max_avg_height}')
                print(f'Clicked island average height: {clicked_island_avg_height}')
                print(f'Clicked position: ({cell_x}, {cell_y})')

                if tries_left <= 0:
                    play = False
                    draw_precision_mode_summary(window, window_width, size, correct_guesses, scale_factor, rows)
                    break

        # Get the mouse position
        mouse_x, mouse_y = pygame.mouse.get_pos()
        hover_pos = (mouse_x, mouse_y)

        # Redraw the window with the hover effect and clicked position
        redraw(window, hover_pos, size, high_res_rows, high_res_map_data, clicked_pos, message, all_island_edges)

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

        pygame.display.update()

    pygame.quit()
    
def draw_precision_mode_summary(window, window_width, size, correct_guesses, scale_factor, rows):
    overlay = pygame.Surface((window_width, size))
    overlay.set_alpha(200)  # Set transparency
    overlay.fill((50, 50, 50))  # Darker color
    window.blit(overlay, (0, 0))

    font = pygame.font.SysFont(None, 72)
    summary_text = font.render("Game Over!", True, (255, 255, 255))
    window.blit(summary_text, (window_width // 2 - summary_text.get_width() // 2, size // 3))

    score_font = pygame.font.SysFont(None, 48)
    score_text = score_font.render(f"Guessed: {correct_guesses}", True, (255, 255, 255))
    window.blit(score_text, (window_width // 2 - score_text.get_width() // 2, size // 2))

    button_font = pygame.font.SysFont(None, 48)
    button_text = button_font.render("Play Again", True, (255, 255, 255))
    button_rect = button_text.get_rect(center=(window_width // 2, size // 1.5))
    pygame.draw.rect(window, (100, 100, 100), button_rect.inflate(20, 10))
    window.blit(button_text, button_rect.topleft)

    pygame.display.update()

    # Wait for the player to click the "Play Again" button
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if button_rect.collidepoint(mouse_x, mouse_y):
                    waiting = False
                    game_loop(window, window_width, size, scale_factor, rows)

def reset_game(scale_factor, rows, window, size):
    # Fetch fresh data
    map_data = fetch_map_data()
    if not map_data:
        return None, None, None, None, False, 3, None, None, None
    high_res_map_data = interpolate_grid(map_data, scale_factor)
    high_res_rows = rows * scale_factor
    clicked_pos = None
    game_started = False
    tries_left = 3
    islands, island_averages = calculate_island_averages(high_res_map_data)
    max_avg_height = max(island_averages) if island_averages else 0
    return map_data, high_res_map_data, high_res_rows, clicked_pos, game_started, tries_left, islands, island_averages, max_avg_height

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

def get_island_edges(island, grid):
    edges = []
    for cx, cy in island:
        for nx, ny in [(cx-1, cy), (cx+1, cy), (cx, cy-1), (cx, cy+1)]:
            if 0 <= nx < len(grid[0]) and 0 <= ny < len(grid) and grid[ny][nx] <= 0:
                edges.append((cx, cy))
                break
    return edges

def flood_fill(grid, x, y, visited, window=None, size=None, rows=None, message=None):
    queue = deque([(x, y)])
    island_cells = []
    if size and rows:
        distanceBtwRows = size / rows  # Use float division to get precise distance
    while queue:
        cx, cy = queue.popleft()
        if (cx, cy) in visited or grid[cy][cx] <= 0:
            continue
        visited.add((cx, cy))
        island_cells.append((cx, cy))
        for nx, ny in [(cx-1, cy), (cx+1, cy), (cx, cy-1), (cx, cy+1)]:
            if 0 <= nx < len(grid[0]) and 0 <= ny < len(grid):
                queue.append((nx, ny))
        # Draw the current cell in red to visualize the flood fill process
        if window and size and rows:
            pygame.draw.rect(window, (255, 0, 0), (cx * distanceBtwRows, cy * distanceBtwRows, distanceBtwRows, distanceBtwRows))
            if message:
                font = pygame.font.SysFont(None, 48)
                message_text = font.render(message, True, (255, 255, 255))
                window.fill((0, 0, 0), (size // 2 - message_text.get_width() // 2, size - 50, message_text.get_width(), message_text.get_height()))
                window.blit(message_text, (size // 2 - message_text.get_width() // 2, size - 50))
            pygame.display.update()
    return island_cells

def calculate_island_averages(grid):
    visited = set()
    islands = []
    island_averages = []
    for y in range(len(grid)):
        for x in range(len(grid[0])):
            if (x, y) not in visited and grid[y][x] > 0:
                island_cells = flood_fill(grid, x, y, visited)  # No visualization during initial calculation
                islands.append(island_cells)
                average_height = sum(grid[cy][cx] for cx, cy in island_cells) / len(island_cells)
                island_averages.append(average_height)
    return islands, island_averages

def draw_starting_screen(window, window_width, size):
    overlay = pygame.Surface((window_width, size))
    overlay.set_alpha(200)  # Set transparency
    overlay.fill((50, 50, 50))  # Darker color
    window.blit(overlay, (0, 0))

    font = pygame.font.SysFont(None, 72)
    title_text = font.render("Isle Of Heights", True, (255, 255, 255))
    window.blit(title_text, (window_width // 2 - title_text.get_width() // 2, size // 3))

    explanation_font = pygame.font.SysFont(None, 36)
    explanation_text = explanation_font.render("Find the island with the greatest average height. You have 3 attempts.", True, (255, 255, 255))
    window.blit(explanation_text, (window_width // 2 - explanation_text.get_width() // 2, size // 2.5))

    button_font = pygame.font.SysFont(None, 48)
    button_text = button_font.render("Play Now!", True, (255, 255, 255))
    button_rect = button_text.get_rect(center=(window_width // 2, size // 2))
    pygame.draw.rect(window, (100, 100, 100), button_rect.inflate(20, 10))
    window.blit(button_text, button_rect.topleft)

    time_trial_text = button_font.render("Time Trial Mode", True, (255, 255, 255))
    time_trial_rect = time_trial_text.get_rect(center=(window_width // 2, size // 1.5))
    pygame.draw.rect(window, (100, 100, 100), time_trial_rect.inflate(20, 10))
    window.blit(time_trial_text, time_trial_rect.topleft)

    precision_mode_text = button_font.render("Precision Mode", True, (255, 255, 255))
    precision_mode_rect = precision_mode_text.get_rect(center=(window_width // 2, size // 1.2))
    pygame.draw.rect(window, (100, 100, 100), precision_mode_rect.inflate(20, 10))
    window.blit(precision_mode_text, precision_mode_rect.topleft)

    return button_rect, time_trial_rect, precision_mode_rect

def draw_game_over_screen(window, window_width, size):
    overlay = pygame.Surface((window_width, size))
    overlay.set_alpha(200)  # Set transparency
    overlay.fill((50, 50, 50))  # Darker color
    window.blit(overlay, (0, 0))

    font = pygame.font.SysFont(None, 72)
    game_over_text = font.render("No Tries Left", True, (255, 255, 255))
    window.blit(game_over_text, (window_width // 2 - game_over_text.get_width() // 2, size // 3))

    button_font = pygame.font.SysFont(None, 48)
    button_text = button_font.render("Try Again", True, (255, 255, 255))
    button_rect = button_text.get_rect(center=(window_width // 2, size // 2))
    pygame.draw.rect(window, (100, 100, 100), button_rect.inflate(20, 10))
    window.blit(button_text, button_rect.topleft)

    return button_rect

def redraw(window, hover_pos, size, rows, map_data, clicked_pos=None, message=None, all_island_edges=None):
    window.fill((0, 0, 0))
    draw_grid(window, size, rows, map_data)
    highlight_cell(window, hover_pos, size, rows)
    draw_color_bar(window, size, get_color_steps())

    # Display the coordinates and value of the clicked cell
    distanceBtwRows = size / rows  # Use float division to get precise distance
    if clicked_pos:
        cell_x = int(clicked_pos[0] // distanceBtwRows)
        cell_y = int(clicked_pos[1] // distanceBtwRows)
        
        if 0 <= cell_x < len(map_data[0]) and 0 <= cell_y < len(map_data):
            cell_value = map_data[cell_y][cell_x]
            print(f'Clicked: {clicked_pos}, Value: {cell_value}')
        else:
            print(f'Clicked: {clicked_pos}, Value: Out of bounds')

    # Draw the edges of all scanned islands in red
    if all_island_edges:
        for island_edges in all_island_edges:
            for edge_x, edge_y in island_edges:
                pygame.draw.rect(window, (255, 0, 0), (edge_x * distanceBtwRows, edge_y * distanceBtwRows, distanceBtwRows, distanceBtwRows), 2)

    # Display the message if there is one
    if message:
        font = pygame.font.SysFont(None, 48)
        message_text = font.render(message, True, (255, 255, 255))
        window.blit(message_text, (size // 2 - message_text.get_width() // 2, size - 50))

    pygame.display.update()

def game_loop(window, window_width, size, scale_factor, rows):
    # Initialize game variables
    map_data, high_res_map_data, high_res_rows, clicked_pos, game_started, tries_left, islands, island_averages, max_avg_height = reset_game(scale_factor, rows, window, size)

    play = True
    message = None
    all_island_edges = []  # List to store edges of all scanned islands
    while play:
        hover_pos = None
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                play = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if not game_started:
                    button_rect, time_trial_rect, precision_mode_rect = draw_starting_screen(window, window_width, size)
                    if button_rect.collidepoint(mouse_x, mouse_y):
                        game_started = True
                    elif time_trial_rect.collidepoint(mouse_x, mouse_y):
                        time_trial_mode(window, window_width, size, scale_factor, rows)
                        return
                    elif precision_mode_rect.collidepoint(mouse_x, mouse_y):
                        precision_mode(window, window_width, size, scale_factor, rows)
                        return
                elif tries_left > 0:
                    clicked_pos = (mouse_x, mouse_y)  # Store the clicked position
                    tries_left -= 1  # Decrease the number of tries left
                    distanceBtwRows = size / high_res_rows  # Use float division to get precise distance
                    cell_x = int(clicked_pos[0] // distanceBtwRows)
                    cell_y = int(clicked_pos[1] // distanceBtwRows)
                    clicked_island_avg_height = None
                    for island, avg_height in zip(islands, island_averages):
                        if (cell_x, cell_y) in island:
                            clicked_island_avg_height = avg_height
                            # Visualize the flood fill process for the clicked island
                            flood_fill(high_res_map_data, cell_x, cell_y, set(), window, size, high_res_rows, "Calculating...")
                            island_edges = get_island_edges(island, high_res_map_data)
                            all_island_edges.append(island_edges)  # Add the edges to the list of all scanned islands
                            if avg_height == max_avg_height:
                                draw_winning_screen(window, window_width, size, scale_factor, rows)
                                return  # Exit the game loop after winning
                            else:
                                message = "Wrong guess. Try again."
                            break
                    print(f'Max average height: {max_avg_height}')
                    print(f'Clicked island average height: {clicked_island_avg_height}')
                    print(f'Clicked position: ({cell_x}, {cell_y})')
                else:
                    if game_over_button_rect.collidepoint(mouse_x, mouse_y):
                        map_data, high_res_map_data, high_res_rows, clicked_pos, game_started, tries_left, islands, island_averages, max_avg_height = reset_game(scale_factor, rows, window, size)
                        message = None
                        all_island_edges = []  # Reset the list of all scanned islands

        # Get the mouse position
        mouse_x, mouse_y = pygame.mouse.get_pos()
        hover_pos = (mouse_x, mouse_y)

        if not game_started:
            button_rect, time_trial_rect, precision_mode_rect = draw_starting_screen(window, window_width, size)
        elif tries_left <= 0:
            game_over_button_rect = draw_game_over_screen(window, window_width, size)
        else:
            # Redraw the window with the hover effect and clicked position
            redraw(window, hover_pos, size, high_res_rows, high_res_map_data, clicked_pos, message, all_island_edges)

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

            if clicked_pos:
                clicked_pos = None

        pygame.display.update()

    pygame.quit()

def draw_time_trial_summary(window, window_width, size, score, scale_factor, rows):
    overlay = pygame.Surface((window_width, size))
    overlay.set_alpha(200)  # Set transparency
    overlay.fill((50, 50, 50))  # Darker color
    window.blit(overlay, (0, 0))

    font = pygame.font.SysFont(None, 72)
    summary_text = font.render("Time's Up!", True, (255, 255, 255))
    window.blit(summary_text, (window_width // 2 - summary_text.get_width() // 2, size // 3))

    score_font = pygame.font.SysFont(None, 48)
    score_text = score_font.render(f"Score: {score}", True, (255, 255, 255))
    window.blit(score_text, (window_width // 2 - score_text.get_width() // 2, size // 2))

    button_font = pygame.font.SysFont(None, 48)
    button_text = button_font.render("Play Again", True, (255, 255, 255))
    button_rect = button_text.get_rect(center=(window_width // 2, size // 1.5))
    pygame.draw.rect(window, (100, 100, 100), button_rect.inflate(20, 10))
    window.blit(button_text, button_rect.topleft)

    pygame.display.update()

    # Wait for the player to click the "Play Again" button
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if button_rect.collidepoint(mouse_x, mouse_y):
                    waiting = False
                    game_loop(window, window_width, size, scale_factor, rows)

def draw_winning_screen(window, window_width, size, scale_factor, rows):
    overlay = pygame.Surface((window_width, size))
    overlay.set_alpha(200)  # Set transparency
    overlay.fill((50, 50, 50))  # Darker color
    window.blit(overlay, (0, 0))

    font = pygame.font.SysFont(None, 72)
    winning_text = font.render("Congratulations!", True, (255, 255, 255))
    window.blit(winning_text, (window_width // 2 - winning_text.get_width() // 2, size // 3))

    message_font = pygame.font.SysFont(None, 48)
    message_text = message_font.render("You found the island with the greatest average height!", True, (255, 255, 255))
    window.blit(message_text, (window_width // 2 - message_text.get_width() // 2, size // 2))

    button_font = pygame.font.SysFont(None, 48)
    button_text = button_font.render("Play Again", True, (255, 255, 255))
    button_rect = button_text.get_rect(center=(window_width // 2, size // 1.5))
    pygame.draw.rect(window, (100, 100, 100), button_rect.inflate(20, 10))
    window.blit(button_text, button_rect.topleft)

    pygame.display.update()

    # Wait for the player to click the "Play Again" button
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if button_rect.collidepoint(mouse_x, mouse_y):
                    waiting = False
                    game_loop(window, window_width, size, scale_factor, rows)
