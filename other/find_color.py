import mss
import numpy as np
import pyautogui
import keyboard

while True:
    # Break the loop if Esc is pressed
    if keyboard.is_pressed('esc'):
        break

    # Find current mouse location
    x, y = pyautogui.position()

    # Define the pixel to monitor
    monitor = {"top": y, "left": x, "width": 1, "height": 1}

    with mss.mss() as sct:   
        # Capture the pixel
        screenshot = sct.grab(monitor)
        # Convert the screenshot to a numpy array
        img = np.array(screenshot)

    # Print colour
    print("RGBA:", img[0, 0])