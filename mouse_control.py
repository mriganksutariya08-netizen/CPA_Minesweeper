import time
from grid_data_refactored import run, DIFFICULTY, BOARD_COORDS
from deterministic_solver import solver_run

from pynput.mouse import Controller, Button
mouse = Controller()


def get_flag_and_safe_from_changes(changes, coord_grid):

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


def left_clicker(coords):
    for (x, y) in coords:
        mouse.position = (x, y)
        mouse.press(Button.left)
        mouse.release(Button.left)
        time.sleep(0.001)

def right_clicker(coords):
    for (x, y) in coords:
        mouse.position = (x, y)
        mouse.press(Button.right)
        mouse.release(Button.right)
        time.sleep(0.001)

def first_click():
    #click thw centre
    tx, ty, rows, cols, tile = BOARD_COORDS[DIFFICULTY]
    cx = tx + (cols // 2) * tile + tile // 2
    cy = ty + (rows // 2) * tile + tile // 2
    mouse.position = (cx, cy)
    mouse.press(Button.left)
    mouse.release(Button.left)


if __name__ == "__main__":
    i = 1
    start = time.perf_counter()
    first_click()
    time.sleep(0.1)


    while True:
        #fresh screenshot
        grid, coord_grid = run(DIFFICULTY)

        time.sleep(0.05)
        changes = solver_run(grid)
        flags, safes = get_flag_and_safe_from_changes(changes, coord_grid)

        print(f"\niteration number {i}")
        print(f"new flags are at: {flags}")
        print(f"new safe tiles are at: {safes}")

        #code breaks in first iteration
        if 1 == 1:
            time.sleep(0.1)

        left_clicker(safes)
        right_clicker(flags)
        #time.sleep(0.1)

        if not flags and not safes:
            print("no more moves possible using rules 1 & 2")
            break

        i += 1
    end = time.perf_counter()
    print(f"\nit took {(end - start):.4f}s")