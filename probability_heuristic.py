# probability_heuristic.py (Modified: score_map and 'F' as open)
from collections import defaultdict
from grid_data import run, DIFFICULTY

DIRS = [(-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1)]

def in_bounds(grid, r, c):
    return 0 <= r < len(grid) and 0 <= c < len(grid[0])

def neighbors(grid, r, c):
    for dr,dc in DIRS:
        rr,cc = r+dr, c+dc
        if in_bounds(grid, rr, cc):
            yield rr,cc

def is_number(cell):
    if isinstance(cell, int): return True
    if isinstance(cell, str) and cell.isdigit(): return True
    return False

def as_int(cell):
    if isinstance(cell, int): return cell
    return int(cell)

def compute_local_probs(grid):
    """
    Return: prob_map for uncovered frontier cells only (dict coord->prob in [0,1])
    (This function remains unchanged as 'F' handling here is correct for mine counting)
    """
    contribs = defaultdict(list)
    rows, cols = len(grid), len(grid[0])
    for r in range(rows):
        for c in range(cols):
            cell = grid[r][c]
            if is_number(cell):
                number = as_int(cell)
                flagged = 0
                unknowns = []
                for (rr,cc) in neighbors(grid, r, c):
                    v = grid[rr][cc]
                    if v == 'F':
                        flagged += 1
                    elif v == '-':
                        unknowns.append((rr,cc))
                rem = number - flagged
                if unknowns and rem >= 0:
                    contrib = rem / len(unknowns)
                    for u in unknowns:
                        contribs[u].append(contrib)
    # aggregate contributions
    prob_map = {}
    for coord, lst in contribs.items():
        prob_map[coord] = sum(lst) / len(lst)
        # clamp safety
        if prob_map[coord] < 0: prob_map[coord] = 0.0
        if prob_map[coord] > 1: prob_map[coord] = 1.0
    return prob_map

# ----------------------------------------------------------------------
# MODIFIED FUNCTION: 'F' now contributes to open_n
# ----------------------------------------------------------------------
def _neighbour_counts(grid, r, c):
    """Return (open_neighbors, unknown_neighbors) around (r,c)."""
    open_n = 0
    unknown_n = 0
    for (rr,cc) in neighbors(grid, r, c):
        v = grid[rr][cc]
        if v == '-':
            unknown_n += 1
        else:
            # treat 'F', numbers, 'S', '0', etc. as open/revealed/known
            open_n += 1
    return open_n, unknown_n
# ----------------------------------------------------------------------

def choose_lowest_prob_cell(grid):
    prob_map = compute_local_probs(grid)
    score_map = {} # Dictionary to hold the final scores

    # if no frontier — fall back to first covered tile
    if not prob_map:
        for r in range(len(grid)):
            for c in range(len(grid[0])):
                if grid[r][c] == '-':
                    return (r,c), score_map
        return None, score_map

    # build candidate list from prob_map keys
    candidates = list(prob_map.keys())

    # prefer candidates that have at least this many opened neighbors
    min_open_thresholds = [ 3, 2, 0]
    filtered = []
    for thr in min_open_thresholds:
        filtered = [coord for coord in candidates if _neighbour_counts(grid, coord[0], coord[1])[0] >= thr]
        if filtered:
            break

    # if still empty, use original candidates
    if not filtered:
        filtered = candidates

    # scoring
    weight_unknown_penalty = 0.4
    best = None
    best_score = float('inf')

    for coord in filtered:
        r,c = coord
        p = prob_map.get(coord, 1.0)
        open_n, unknown_n = _neighbour_counts(grid, r, c)
        # penalty normalized by max neighbours (8)
        penalty = weight_unknown_penalty * (unknown_n / 8.0)
        score = p + penalty

        # Store the calculated score
        score_map[coord] = score

        # tie-break logic (minimizing score)
        if score < best_score - 1e-9:
            best_score = score
            best = coord
        elif abs(score - best_score) < 1e-9:
            # tie-breaker on numeric neighbor count
            cur_num_neighbors = sum(1 for (rr,cc) in neighbors(grid, r, c) if is_number(grid[rr][cc]))
            best_num_neighbors = sum(1 for (rr,cc) in neighbors(grid, best[0], best[1]) if is_number(grid[rr][cc]))
            if cur_num_neighbors < best_num_neighbors:
                best = coord

    # sanity: ensure best is a covered tile
    if best is None or grid[best[0]][best[1]] != '-':
        return None, score_map

    # Return the chosen best coordinate and the map of all scores
    return best, score_map

if __name__ == "__main__":
    grid = run(DIFFICULTY)[0]
    best, score_map = choose_lowest_prob_cell(grid)
    print(f"score map is {score_map}\nand the best tile is {best}")