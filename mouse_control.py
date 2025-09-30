import time
from pynput.mouse import Controller, Button
from grid_data import DIFFICULTY, BOARD_COORDS
mouse = Controller()


def get_flags_and_safes_locations(changes, coord_grid):

    flag_positions = []
    safe_positions = []
    rows = len(changes)
    cols = len(changes[0]) if rows else 0

    for r in range(rows):
        for c in range(cols):
            cell = changes[r][c]
            if cell == "F":
                flag_positions.append(coord_grid[r][c])
            elif cell == "S":
                safe_positions.append(coord_grid[r][c])

    return flag_positions, safe_positions

def grid_to_coords(grid_position, coord_grid):
    r, c = grid_position
    return coord_grid[r][c]

def left_clicker(coords):
    for (x, y) in coords:
        mouse.position = (x, y)
        mouse.press(Button.left)
        mouse.release(Button.left)
        time.sleep(0.007)

def right_clicker(coords):
    for (x, y) in coords:
        mouse.position = (x, y)
        mouse.press(Button.right)
        mouse.release(Button.right)
        time.sleep(0.007)

def first_click():
    tx, ty, rows, cols, tile = BOARD_COORDS[DIFFICULTY]
    cx = tx + (cols // 2) * tile + tile // 2
    cy = ty + (rows // 2) * tile + tile // 2
    mouse.position = (cx, cy)
    mouse.press(Button.left)
    mouse.release(Button.left)
