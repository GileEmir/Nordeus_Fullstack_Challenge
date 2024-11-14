import pygame
from grid import draw_grid, highlight_cell, draw_color_bar, get_color_steps

def redraw(window, hover_pos, size, rows, map_data, clicked_pos=None):
    window.fill((0, 0, 0))
    draw_grid(window, size, rows, map_data)
    highlight_cell(window, hover_pos, size, rows)
    draw_color_bar(window, size, get_color_steps())

    # Display the coordinates and value of the clicked cell
    if clicked_pos:
        distanceBtwRows = size / rows  # Use float division to get precise distance
        cell_x = int(clicked_pos[0] // distanceBtwRows)
        cell_y = int(clicked_pos[1] // distanceBtwRows)
        
        if 0 <= cell_x < len(map_data[0]) and 0 <= cell_y < len(map_data):
            cell_value = map_data[cell_y][cell_x]
            print(f'Clicked: {clicked_pos}, Value: {cell_value}')
        else:
            print(f'Clicked: {clicked_pos}, Value: Out of bounds')

    pygame.display.update()