import pyautogui
import time

#delay start
timer = 5
for i in range(timer,0,-1):
    print(f'{i}...')
    time.sleep(1)


x,y = pyautogui.position()
pixel_color = pyautogui.screenshot().getpixel((x, y))

print(f"x coord is: {x}\ny coord is: {y}")
print(f"Pixel color at ({x}, {y}) is: {pixel_color}")