# remember to zoom to 50% and use in 50-50 splitscreen
import mss
import numpy as np
import pyautogui
import keyboard

# for speed
#pyautogui.FAILSAFE = False
pyautogui.PAUSE = 0.025 # set 0.0 for speed, but then it won't stop at 30
pyautogui.MINIMUM_DURATION = 0.0

# Define the target colors
target_color = np.array([232, 195, 149])  
target_colour = np.array([255, 255, 255]) 

# Define the pixel to monitor
monitor = {"top": 200, "left": 170, "width": 600, "height": 280}

# Start the test
pyautogui.click(470, 340)

# Initialize the counter
counter = 0

# Start an infinite loop
while True:
    # Break the loop if Esc is pressed
    if keyboard.is_pressed('esc') or counter >= 30: # remove counter for max speed due to double clicks
        break

    with mss.mss() as sct:   
        # Capture the screenshot
        screenshot = sct.grab(monitor)
        # Convert the screenshot to a numpy array
        img = np.array(screenshot)

        # Initialize the flag
        found = False

        # Iterate over the pixels in the image
        for y in range(0, img.shape[0], 20):
            for x in range(0, img.shape[1], 20):

                # If the pixel color matches the target color
                if np.array_equal(img[y, x][:3], target_color) or np.array_equal(img[y, x][:3], target_colour):
                    
                    #print(f"Checked {counter} pixels.") Debugging line

                    # Click the pixel
                    pyautogui.click(monitor['left'] + x, monitor['top'] + y)

                    counter += 1

                    # Set the flag to True and break the inner loop
                    found = True
                    break

            # If the target color was found, break the outer loop
            if found:
                break