import PIL
import pyautogui
import time

# A dictionary to store Minesweeper board values
# colors from minesweeperonline.com
# only beginner value works on my laptop rn

board_coords = {
    "beginner": {
        "top_left": (484, 282),
        "rows_column": (9, 9),
        "tile_size": 32
    },
    "intermediate": {
        "top_left": (492, 248),
        "rows_column": (16, 16),
        "tile_size": 32
    },
    "advanced": {
        "top_left": (258, 254),
        "rows_column": (16, 30),
        "tile_size": 32
    },
    "custom1": {
        "top_left": (148, 486),
        "rows_column": (16, 30),
        "tile_size": 48
    }

}

difficulty = "custom1"

# delay start
timer = 2
for i in range(timer, 0, -1):
    print(f'{i}...')
    time.sleep(1)

top_left_x, top_left_y = board_coords[difficulty]["top_left"]
rows, columns = board_coords[difficulty]["rows_column"]
tile_size = board_coords[difficulty]["tile_size"]

bottom_right_x = top_left_x + columns * tile_size
bottom_right_y = top_left_y + rows * tile_size

width = bottom_right_x - top_left_x
height = bottom_right_y - top_left_y

print("Top left:", (top_left_x, top_left_y))
print("Bottom right:", (bottom_right_x, bottom_right_y))
print("Board size:", (width, height))

game_region = (top_left_x, top_left_y, width, height)
screenshot1 = pyautogui.screenshot(region=game_region)

#define grid size
rows, columns = board_coords[difficulty]["rows_column"]


def make_pixel_grid(image):
    image = PIL.Image.frombytes("RGB", image.size, image.tobytes())
    grid = []
    for row in range(rows):
        grid_row = []
        for column in range(columns):
            # the pixel to consider
            x1 = column * tile_size + (tile_size * 1 / 16)
            x = column * tile_size + (tile_size * 7 / 16)
            y = row * tile_size + (tile_size * 12 / 16)

            pixel = image.getpixel((x, y))

            if pixel == (189, 189, 189):
                # check if it is opened or unopened
                corner_pixel = image.getpixel((x1, y))
                if corner_pixel == (255, 255, 255):
                    value = '-'
                else:
                    value = '0'
                    #value = str(pixel)

            # assign values to colors
            elif pixel == (0, 0, 255):
                value = '1'
            elif pixel == (0, 123, 0):
                value = '2'
            elif pixel == (255, 0, 0):
                value = '3'
            elif pixel == (0, 0, 123):
                value = '4'




            else:
                #value = 'ND'
                value = str(pixel)

            # make final grid
            grid_row.append(value)
        grid.append(grid_row)

    # print the grid
    for row in grid:
        print(" ".join(row))

    return grid


grid = make_pixel_grid(screenshot1)
print(grid)


def get_neighbours(row, column):
    #neighboring values from top left clockwise
    neighbours = []
    for i in range(-1, 2, 1):
        neighbours.append(grid[row - 1][column + i])
    neighbours.append(grid[row][column + 1])

    for i in range(-1, 2, 1):
        neighbours.append(grid[row + 1][column - i])
    neighbours.append(grid[row][column - 1])

    return neighbours


print(f'neighbours: {get_neighbours(2, 1)}')

def get_tile_row_colors(image, row, col, y_offset, tile_size):
    image = PIL.Image.frombytes("RGB", image.size, image.tobytes())
    colors = []
    # compute tile top-left (relative to cropped image)
    tile_x = col * tile_size
    tile_y = row * tile_size

    for x in range(tile_size):
        pixel = image.getpixel((tile_x + x, tile_y + y_offset))
        colors.append(pixel)

    return colors

row_colors = get_tile_row_colors(screenshot1, row=0, col=4, y_offset=8, tile_size=16)

print(row_colors)
