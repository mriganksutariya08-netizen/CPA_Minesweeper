import pyautogui
import time
'''
use this file to get the values for the top_left_x and top_left_y
note that you are supposed to hover your mouse on the corner of the tile and not the board
please take a few readings as an error here will render the code dysfunctional
'''


#delay start
timer = 4
for i in range(timer,0,-1):
    print(f'{i}...')
    time.sleep(1)


x,y = pyautogui.position()
pixel_color = pyautogui.screenshot().getpixel((x, y))

print(f"x coord is: {x}\ny coord is: {y}")

print(f"Pixel color at ({x}, {y}) is: {pixel_color}")