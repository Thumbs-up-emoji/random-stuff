# tried automating it so it would click for the next attempt as well, idt that's worth it tho
import mss
import numpy as np
import pyautogui

# Define the pixel to monitor
monitor = {"top": 500, "left": 200, "width": 1, "height": 1}

with mss.mss() as sct:
    while True:
        # Capture the pixel
        screenshot = sct.grab(monitor)

        # Convert the screenshot to a numpy array
        img = np.array(screenshot)
        
        # print(img) debugging line
        # print(screenshot) debugging line

        # Check the pixel
        if np.all(img[0, 0][:3] == [106, 219, 75]):
            # Click without moving the mouse
            print("Green!")
            pyautogui.click()
            break