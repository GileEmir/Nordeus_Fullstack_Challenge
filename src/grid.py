import pygame


def draw_color_bar(window, size, color_steps):
    bar_width = 100
    padding = 20
    text_padding = 10  # Reduced padding for text
    top_bottom_padding = 20  # Padding at the top and bottom of the color bar
    available_height = size - 2 * top_bottom_padding  # Height available for the color bar
    step_height = available_height // len(color_steps)
    grid_size = size  # The size of the grid area
    font = pygame.font.SysFont(None, 24)
    
    # Define the value ranges for each color step based on the get_color function
    value_ranges = [
        "Deep Water",  # -1
        "Shallow Water",  # 0
        "1 - 49",  # 1-49
        "50 - 99",  # 50-99
        "100 - 149",  # 100-149
        "150 - 199",  # 150-199
        "200 - 249",  # 200-249
        "250 - 299",  # 250-299
        "300 - 349",  # 300-349
        "350 - 399",  # 350-399
        "400 - 449",  # 400-449
        "450 - 499",  # 450-499
        "500 - 549",  # 500-549
        "550 - 599",  # 550-599
        "600 - 649",  # 600-649
        "650 - 699",  # 650-699
        "700 - 749",  # 700-749
        "750 - 799",  # 750-799
        "800 - 849",  # 800-849
        "850 - 899",  # 850-899
        "900 - 949",  # 900-949
        "950 - 999",  # 950-999
        "Mountain - White"  # 1000
    ]
    
    for i, color in enumerate(color_steps):
        pygame.draw.rect(window, color, (grid_size + padding, top_bottom_padding + i * step_height, bar_width, step_height))
        
        # Create the label text showing the range for each color step
        value_text = font.render(value_ranges[i], True, (255, 255, 255))  # Set text color to white
        
        # Position the text next to each color block
        text_x = grid_size + padding + bar_width + text_padding
        text_y = top_bottom_padding + i * step_height + step_height // 2 - 12
        window.blit(value_text, (text_x, text_y))
    
    
def get_color_steps():
    return [
        (0, 0, 169),       # Water - Dark Blue
        (0, 0, 255),       # Water - Light Blue
        (34, 139, 34),     # Light Green
        (50, 205, 50),     # Lime Green
        (60, 179, 113),    # Medium Sea Green
        (85, 107, 47),     # Dark Olive Green
        (107, 142, 35),    # Olive Drab
        (139, 69, 19),     # Saddle Brown
        (160, 82, 45),     # Sienna
        (205, 133, 63),    # Peru
        (210, 105, 30),    # Chocolate
        (222, 184, 135),   # Burlywood
        (245, 222, 179),   # Wheat
        (255, 228, 196),   # Bisque
        (255, 218, 185),   # Peach Puff
        (255, 228, 181),   # Moccasin
        (255, 239, 213),   # Papaya Whip
        (255, 245, 238),   # Seashell
        (255, 250, 240),   # Floral White
        (255, 255, 255),   # White (Mountain)
    ]

def draw_grid(window, size, rows, map_data, line_color=(200, 200, 200)):
    distanceBtwRows = size / rows  # Use float division to get precise distance
    cols = len(map_data[0])  # Number of columns
    for i in range(rows):
        for j in range(cols):
            value = map_data[i][j]
            color = get_color(value)
            x = round(j * distanceBtwRows)
            y = round(i * distanceBtwRows)
            width = round((j + 1) * distanceBtwRows) - x
            height = round((i + 1) * distanceBtwRows) - y
            pygame.draw.rect(window, color, (x, y, width, height))

    # Draw the grid lines separately with specified color
    for i in range(rows + 1):
        x = round(i * distanceBtwRows)
        y = round(i * distanceBtwRows)
        pygame.draw.line(window, line_color, (x, 0), (x, size), 1)
        pygame.draw.line(window, line_color, (0, y), (size, y), 1)

def get_color(value):
    # Define the color steps in the range 0 to 1000, divided into 20 levels
    color_steps = [
        (0, 0, 169),       # Water - Dark Blue
        (0, 0, 255),       # Water - Light Blue
        (34, 139, 34),     # Light Green
        (50, 205, 50),     # Lime Green
        (60, 179, 113),    # Medium Sea Green
        (85, 107, 47),     # Dark Olive Green
        (107, 142, 35),    # Olive Drab
        (139, 69, 19),     # Saddle Brown
        (160, 82, 45),     # Sienna
        (205, 133, 63),    # Peru
        (210, 105, 30),    # Chocolate
        (222, 184, 135),   # Burlywood
        (245, 222, 179),   # Wheat
        (255, 228, 196),   # Bisque
        (255, 218, 185),   # Peach Puff
        (255, 228, 181),   # Moccasin
        (255, 239, 213),   # Papaya Whip
        (255, 245, 238),   # Seashell
        (255, 250, 240),   # Floral White
        (255, 255, 255),   # White (Mountain)
    ]
    
    # Handle water (value 0) and darker water (value -1)
    if value == 0:
        return color_steps[1]  # Light Blue for water
    elif value == -1:
        return color_steps[0]  # Dark Blue for darker water
    
    # Handle mountain (value 1000)
    if value == 1000:
        return color_steps[19]  # White (for mountain top)
    
    # Map the value to one of the 20 color steps for values above 0
    if value > 0:
        step = min(int((value - 1) // 50) + 2, 19)  # Adjust step calculation to avoid blue colors
        return color_steps[step]
    
    # Default case for unexpected values
    return (255, 0, 0)  # Red for unexpected values (should not be used)

def highlight_cell(window, hover_pos, size, rows, line_color=(255, 0, 0)):
    if hover_pos:
        distanceBtwRows = size / rows  # Use float division to get precise distance
        x, y = hover_pos
        cell_x = round((x // distanceBtwRows) * distanceBtwRows)
        cell_y = round((y // distanceBtwRows) * distanceBtwRows)

        # Draw a thicker border around the highlighted cell
        pygame.draw.rect(window, line_color, (cell_x, cell_y, round(distanceBtwRows), round(distanceBtwRows)), 3)

        # Highlight adjacent cells
        adjacent_cells = [
            (cell_x - distanceBtwRows, cell_y),  # Left
            (cell_x + distanceBtwRows, cell_y),  # Right
            (cell_x, cell_y - distanceBtwRows),  # Up
            (cell_x, cell_y + distanceBtwRows)   # Down
        ]

        for adj_x, adj_y in adjacent_cells:
            if 0 <= adj_x < size and 0 <= adj_y < size:
                pygame.draw.rect(window, line_color, (adj_x, adj_y, round(distanceBtwRows), round(distanceBtwRows)), 2)