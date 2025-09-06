import pyautogui
import time

time.sleep(5)

x,y = pyautogui.position()

pixel_color = pyautogui.screenshot().getpixel((x, y))


print(f"x coord is: {x}\ny coord is: {y}")
print(f"Pixel color at ({x}, {y}) is: {pixel_color}")