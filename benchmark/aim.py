import mss
import numpy as np
import pyautogui
import keyboard

# Define the target color
target_color = (232, 195, 149)  
target_colour = (255, 255, 255) 
# Define the pixel to monitor
monitor = {"top": 200, "left": 170, "width": 600, "height": 280}

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

        # Iterate over the pixels in the image
        for y in range(0, img.shape[0], 30):
            for x in range(0, img.shape[1], 30):
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

                    # Break the inner for loop
                    break
            else:
                # If the target color was not found in the current row, continue with the next row
                continue
            # If the target color was found and clicked, break the outer for loop
            break
        # If the target color was not found in the entire screenshot, continue with the next screenshot
        continue