import pyautogui
import PIL
import time


# A dictionary to store Minesweeper board corners
# values 200% zoom of minesweeperonline.com in a firefox window
board_coords = {
    "beginner": {
        "top_left": (484, 282),
        "bottom_right": (772, 570),
        "rows_column": (9, 9)
    },
    "intermediate": {
        "top_left": (492, 248),
        "bottom_right": (1004, 760),
        "rows_column": (16, 16)
    },
    "advanced": {
        "top_left": (472, 248),
        "bottom_right": (1432, 760),
        "rows_column": (16, 30)
    }
}
difficulty = "beginner"
tile_size = 32

#delay start
timer = 3
for i in range(timer, 0, -1):
    print(f'{i}...')
    time.sleep(1)

#take screenshot
top_left_x, top_left_y = board_coords[difficulty]["top_left"]
bottom_right_x, bottom_right_y = board_coords[difficulty]["bottom_right"]

width = bottom_right_x - top_left_x
height = bottom_right_y - top_left_y

game_region = (top_left_x, top_left_y, width, height)
screenshot = pyautogui.screenshot(region=game_region)
image = PIL.Image.frombytes("RGB", screenshot.size, screenshot.tobytes())
#define grid size
rows, columns = board_coords[difficulty]["rows_column"]

grid = []
for row in range(rows):
    grid_row = []
    for column in range(columns):
        #the pixel to consider
        x = column * tile_size + (tile_size - 18)
        y = row * tile_size + (tile_size - 6)
        pixel = image.getpixel((x, y))

        if pixel == (189, 189, 189):
            #check if it is opened or unopened
            corner_pixel = image.getpixel((x - 14, y - 0))
            if corner_pixel == (255, 255, 255):
                value = '-'
            else:
                value = '0'

        #assign values to colors
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


        #make final grid
        grid_row.append(value)
    grid.append(grid_row)

#print the grid
for row in grid:
    print(" ".join(row))

#print(grid)


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


#print(get_neighbours(5, 6))

