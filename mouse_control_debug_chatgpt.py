import time
import traceback
from grid_data_refactored import run, DIFFICULTY, BOARD_COORDS
from deterministic_solver import solver_run

from pynput.mouse import Controller, Button
mouse = Controller()


def get_flag_and_safe_from_changes(changes, coord_grid):
    """
    Parse the solver *change map* (output of solver_run) once and
    return absolute coordinates for flags and safes.
    """
    flag_positions = []
    safe_positions = []

    # basic validation of changes
    if changes is None:
        raise ValueError("solver_run returned None for changes")

    rows = len(changes)
    if rows == 0:
        return flag_positions, safe_positions

    cols = len(changes[0])

    # validate coord_grid shape
    if not coord_grid or len(coord_grid) != rows or any(len(row) != cols for row in coord_grid):
        raise ValueError(f"coord_grid shape mismatch with changes: changes={rows}x{cols}, "
                         f"coord_grid={'None' if coord_grid is None else f'{len(coord_grid)}x{len(coord_grid[0]) if coord_grid else 0}'}")

    for r in range(rows):
        for c in range(cols):
            cell = changes[r][c]
            if cell == "F":
                flag_positions.append(coord_grid[r][c])
            elif cell == "S":
                safe_positions.append(coord_grid[r][c])

    return flag_positions, safe_positions


def _to_int_coord(coord):
    """Ensure coordinate is a (int, int) tuple and not None-ish."""
    if coord is None:
        raise ValueError("Encountered None coordinate in coord_grid")
    x, y = coord
    return int(round(x)), int(round(y))


def left_clicker(coords):
    for (x, y) in coords:
        xi, yi = _to_int_coord((x, y))
        mouse.position = (xi, yi)
        mouse.press(Button.left)
        mouse.release(Button.left)


def right_clicker(coords):
    for (x, y) in coords:
        xi, yi = _to_int_coord((x, y))
        mouse.position = (xi, yi)
        mouse.press(Button.right)
        mouse.release(Button.right)


def first_click():
    # click the centre
    tx, ty, rows, cols, tile = BOARD_COORDS[DIFFICULTY]
    cx = tx + (cols // 2) * tile + tile // 2
    cy = ty + (rows // 2) * tile + tile // 2
    cx_i, cy_i = int(round(cx)), int(round(cy))
    mouse.position = (cx_i, cy_i)
    mouse.press(Button.left)
    mouse.release(Button.left)


if __name__ == "__main__":
    i = 1
    try:
        first_click()
        time.sleep(0.01)

        while True:
            # fresh screenshot / parse board
            grid, coord_grid = run(DIFFICULTY)

            # safety debug: make sure grid & coord_grid exist
            if grid is None:
                print("run(DIFFICULTY) returned None for grid — exiting.")
                break
            if coord_grid is None:
                print("run(DIFFICULTY) returned None for coord_grid — exiting.")
                break

            # run solver
            changes = solver_run(grid)

            # debug: show a tiny preview if changes is a large grid
            if changes is None:
                print(f"[iter {i}] solver_run returned None. grid size: {len(grid)}x{len(grid[0]) if grid else 0}")
            else:
                print(f"[iter {i}] solver_run returned changes with shape {len(changes)}x{len(changes[0]) if changes else 0}")

            # try to extract flags/safes, with validation inside the function
            try:
                flags, safes = get_flag_and_safe_from_changes(changes, coord_grid)
            except Exception as e:
                print(f"[iter {i}] ERROR while parsing changes -> flags/safes: {e}")
                traceback.print_exc()
                break

            print(f"iteration number {i}")
            print(f"new flags are at: {flags[:10]}{' ...' if len(flags) > 10 else ''}")   # preview up to 10
            print(f"new safe tiles are at: {safes[:10]}{' ...' if len(safes) > 10 else ''}") # preview up to 10

            # click (coords already validated inside clickers)
            if safes:
                left_clicker(safes)
            if flags:
                right_clicker(flags)

            if not flags and not safes:
                print("no more moves possible using rules 1 & 2")
                break

            i += 1

    except Exception as e:
        print("Unhandled exception in main loop:")
        traceback.print_exc()
