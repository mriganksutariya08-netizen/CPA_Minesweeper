#!/usr/bin/env python3
"""
Simplified Minesweeper board sampler (no dataclasses, no typing).
- Keeps the original sampling logic and color mappings.
- Easier to read for school projects.
- Uses PIL (Pillow) and pyautogui for screenshots.
"""

import time
import pyautogui

# -----------------------
# Board definitions
# -----------------------
# Each entry: (top_left_x, top_left_y, rows, cols, tile_size)
BOARD_COORDS = {
    "beginner":  (260, 158, 9,  9,  32),
    "intermediate": (260, 158, 16, 16, 32),
    "advanced":  (258, 254, 16, 30, 32),
    "custom1":   (260, 158, 20, 30, 32),
}

# default difficulty you can change
DIFFICULTY = "custom1"
FLAG_NUMBER = 100

# color -> value mapping (exact RGB matches)
COLOR_VALUE_MAP = {
    (189, 189, 189): None,  # special-case in code
    (0, 0, 255): "1",
    (0, 123, 0): "2",
    (255, 0, 0): "3",
    (0, 0, 123): "4",
    (123, 0, 0): "5",
    (0, 123, 123): "6",
    (0, 0, 0): "7",
    (123, 123, 123): "8"
}

# -----------------------
# Small helpers
# -----------------------
def print_board_info():
    tx, ty, rows, cols, tile = BOARD_COORDS[DIFFICULTY]
    br_x = tx + cols * tile
    br_y = ty + rows * tile
    print("Top-left:", (tx, ty))
    print("Bottom-right:", (br_x, br_y))
    print("Board width x height:", (cols * tile, rows * tile))


def countdown(seconds):
    """Simple blocking countdown before taking screenshot."""
    for i in range(seconds, 0, -1):
        print(i, "...")
        time.sleep(1)

def occurrence_counter(grid, v):
    return sum(1 for row in grid for value in row if value == v)

# -----------------------
# Absolute pixel coords
# -----------------------
def real_coord_grid(board):
    """
    Return a 2D list where each element is the absolute screen coordinate
    (x, y) of the sample pixel for that tile.
    """
    tx, ty, rows, cols, tile = board
    coords = []
    for r in range(rows):
        row_coords = []
        for c in range(cols):
            (mx, my), _ = sample_coords(c, r, tile)
            # add top-left offset to get real screen coords
            abs_x = tx + mx
            abs_y = ty + my
            row_coords.append((abs_x, abs_y))
        coords.append(row_coords)
    return coords

# -----------------------
# Screenshot & sampling
# -----------------------
def capture_board_screenshot(board):
    """Take a screenshot cropped to the board rectangle and return a PIL image."""
    tx, ty, rows, cols, tile = board
    width = cols * tile
    height = rows * tile
    return pyautogui.screenshot(region=(tx, ty, width, height))


def sample_coords(col, row, tile):
    """
    Return two pixel coordinates inside a tile (relative to cropped board image):
      - main sample: used to read the tile color
      - corner sample: used when color is the grey (189,189,189) to disambiguate
    """
    base_x = col * tile
    base_y = row * tile
    sample_x = int(base_x + (10 * tile) / 16)
    corner_x = int(base_x + (2 * tile) / 16)
    sample_y = int(base_y + (12 * tile) / 16)
    corner_y = int(base_y + (2 * tile) / 16)
    return (sample_x, sample_y), (corner_x, corner_y)


# -----------------------
# Grid parsing
# -----------------------
def make_pixel_grid(img, board):
    """Build and return a grid (list of lists) of strings representing tiles."""
    tx, ty, rows, cols, tile = board
    grid = []

    for r in range(rows):
        row_vals = []
        for c in range(cols):
            (mx, my), (cx, cy) = sample_coords(c, r, tile)
            pixel = img.getpixel((mx, my))

            if pixel == (189, 189, 189):
                # check the corner pixel to decide between '-' or '0'
                corner_pixel = img.getpixel((cx, cy))
                if corner_pixel == (255, 255, 255):
                    value = "-"
                else:
                    value = "0"
            elif pixel == (0, 0, 0):
                # check the corner pixel to decide between 'F' or '7'
                corner_pixel = img.getpixel((cx, cy))
                if corner_pixel == (255, 255, 255):
                    value = "F"
                elif corner_pixel == (255, 0, 0):
                    value = "M"
                else:
                    value = "7"

            else:
                mapped = COLOR_VALUE_MAP.get(pixel)
                if mapped is not None:
                    value = mapped
                else:
                    # unknown color; keep raw RGB (good for debugging)
                    value = str(pixel)

            row_vals.append(value)
        grid.append(row_vals)

    return grid

def grid_print(grid):
    for row in grid:
        print(" ".join(row))

# -----------------------
# Neighbour helper
# -----------------------
def get_neighbours(r, c, grid):
    """Return a list of up to 8 neighbour values for tile (r, c)."""
    neighbours = []
    max_r = len(grid)
    max_c = len(grid[0]) if max_r else 0
    directions = [(-1,-1), (-1,0), (-1,1), (0,1), (1,1), (1,0), (1,-1), (0,-1)]
    for dr, dc in directions:
        nr, nc = r + dr, c + dc
        if 0 <= nr < max_r and 0 <= nc < max_c:
            neighbours.append(grid[nr][nc])
        else:
            neighbours.append('x')
    return neighbours


# -----------------------
# Main runner
# -----------------------
def run(difficulty=DIFFICULTY):
    if difficulty not in BOARD_COORDS:
        raise KeyError("Unknown difficulty: {}. Options: {}".format(difficulty, list(BOARD_COORDS.keys())))
    board = BOARD_COORDS[difficulty]
    countdown(0)
    img = capture_board_screenshot(board)
    grid = make_pixel_grid(img, board)
    abs_px_grid = real_coord_grid(board)
    return grid, abs_px_grid


if __name__ == "__main__":
    print_board_info()
    grid = run(DIFFICULTY)[0]
    grid_print(grid)
