


from grid_data import run, get_neighbours, DIFFICULTY, grid_print

'''if the number of hidden tiles equals the number, all are flags'''
def apply_rule1(grid):
    new_grid = [row[:] for row in grid]
    rows = len(grid)
    cols = len(grid[0]) if rows else 0

    for r in range(rows):
        for c in range(cols):
            tile = grid[r][c]

            # act only on numbered tiles
            if tile in ["1","2","3","4","5","6","7","8"]:
                neighbours = get_neighbours(r, c, grid)
                #print(neighbours)
                hidden_count = neighbours.count('-')
                flag_count = neighbours.count('F')


                # when hidden_count == tile, we mark those '-' as 'F'.
                if hidden_count + flag_count == int(tile):
                    directions = [(-1,-1), (-1,0), (-1,1),
                                  (0,1), (1,1), (1,0),
                                  (1,-1), (0,-1)]
                    for dr, dc in directions:
                        nr, nc = r + dr, c + dc
                        if 0 <= nr < rows and 0 <= nc < cols:
                            if grid[nr][nc] == "-":
                                new_grid[nr][nc] = "F"

    return new_grid


'''if number of flags equals the number, all other unopened tiles are safe 'S' '''
def apply_rule2(grid):
    new_grid = [row[:] for row in grid]
    rows = len(grid)
    cols = len(grid[0]) if rows else 0

    for r in range(rows):
        for c in range(cols):
            tile = grid[r][c]

            # act only on numbered tiles
            if tile in ["1","2","3","4","5","6","7","8"]:
                neighbours = get_neighbours(r, c, grid)
                #print(neighbours)

                flag_count = neighbours.count('F')
                # when flag_count == tile, we mark the '-' as 'S'.

                if flag_count == int(tile):
                    directions = [(-1,-1), (-1,0), (-1,1),
                                  (0,1), (1,1), (1,0),
                                  (1,-1), (0,-1)]
                    for dr, dc in directions:
                        nr, nc = r + dr, c + dc
                        if 0 <= nr < rows and 0 <= nc < cols:
                            if grid[nr][nc] == "-":
                                new_grid[nr][nc] = "S"
    return new_grid


"""
take two lists of same size and compare them
return the value of the second in case of difference
else append '-'
"""
def change_map(grid1, grid2):
    changes = []
    rows = len(grid1)
    cols = len(grid1[0])
    for r in range(rows):
        row_changes = []
        for c in range(cols):
            if grid1[r][c] != grid2[r][c]:
                row_changes.append(grid2[r][c])
            else:
                row_changes.append('-')
        changes.append(row_changes)

    return changes

def solver_run(grid):
    updated_grid= apply_rule1(grid)
    updated_grid = apply_rule2(updated_grid)


    return change_map(grid, updated_grid)


if __name__ == "__main__":
    grid = run(DIFFICULTY)[0]
    grid_print(solver_run(grid))

