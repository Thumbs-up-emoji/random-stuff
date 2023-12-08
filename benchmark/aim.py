# optimise for speed
import mss
import numpy as np
import pyautogui
import keyboard

# for speed
pyautogui.FAILSAFE = False
pyautogui.PAUSE = 0.0
pyautogui.MINIMUM_DURATION = 0.0

# Define the target colors
target_color = (232, 195, 149)  
target_colour = (255, 255, 255) 

# Define the pixel to monitor
monitor = {"top": 200, "left": 170, "width": 600, "height": 280}

# Start the test
pyautogui.click(470, 340)

# Initialize the counter
counter = 0

# Start an infinite loop
while True:
    # Break the loop if Esc is pressed
    if keyboard.is_pressed('esc'):
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
                # Increment the counter
                counter += 1

                # If the pixel color matches the target color
                if tuple(img[y, x][:3]) == target_color or tuple(img[y, x][:3]) == target_colour:
                    # Print the number of pixels checked
                    print(f"Checked {counter} pixels.")

                    # Move the mouse to the pixel and click it
                    pyautogui.moveTo(monitor['left'] + x, monitor['top'] + y)
                    pyautogui.click()

                    # Reset the counter
                    counter = 0

                    # Set the flag to True and break the inner loop
                    found = True
                    break

            # If the target color was found, break the outer loop
            if found:
                break