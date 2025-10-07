import time
from mouse_control import left_clicker, right_clicker, first_click, get_flags_and_safes_locations, grid_to_coords
from deterministic_solver import solver_run
from grid_data import run, grid_print, occurrence_counter, DIFFICULTY, FLAG_NUMBER
from probability_heuristic import choose_lowest_prob_cell

i = 1
j = 0
prob_call = 0
flags_found = []
start = time.perf_counter()
first_click()
time.sleep(0.1)

while True:
    iter_start = time.perf_counter()
    # fresh screenshot
    grid, coord_grid = run(DIFFICULTY)

    if occurrence_counter(grid, "M") != 0:
        print("\noops, mb vro")
        break

    time.sleep(0.05)
    changes = solver_run(grid)
    flags, safes = get_flags_and_safes_locations(changes, coord_grid)
    #flags_found += len(flags)

    for item in flags:
        if item not in flags_found:
            flags_found.append(item)

    print(f"\niteration  {i}")
    print(f"new flags are at: {flags}")
    print(f"new safe tiles are at: {safes}")
    print(f"number of flags found: {len(flags_found)}")
    grid_print(changes)

    # code breaks in first iteration
    time.sleep(0.05)

    if not flags and not safes:
        print("no more moves possible using rules 1 & 2")
        # fallback to probability heuristic
        lowest_prob, prob_map = choose_lowest_prob_cell(grid)
        print(prob_map)
        print(f"lowest probability cell is {lowest_prob}")
        if lowest_prob:
            safes.append(grid_to_coords(lowest_prob, coord_grid))
            prob_call += 1
        else:
            break

    right_clicker(flags)
    left_clicker(safes)
    time.sleep(0.05)

    if len(flags_found) >= FLAG_NUMBER:
        j += 1
        if j == 2:
            print("breaking loop")
            break

    i += 1
    print(f"time: {(time.perf_counter() - iter_start):.4f}s")

end = time.perf_counter()
print(f"called probability function {prob_call} times")
print(f"\nit took {(end - start):.4f}s")