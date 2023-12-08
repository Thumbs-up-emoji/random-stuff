# Import the necessary libraries
from PIL import ImageGrab
import pyautogui
import keyboard

# Define the target colors
target_color1 = (149, 195, 232)  
target_color2 = (255, 255, 255)  

# Define the pixel to monitor
monitor = {"top": 200, "left": 170, "width": 600, "height": 280}

# Initialize the counter
counter = 0

# Start an infinite loop
while True:
    # Break the loop if Esc is pressed
    if keyboard.is_pressed('esc'):
        break

    # Capture the screenshot
    screenshot = ImageGrab.grab(bbox=(monitor['left'], monitor['top'], monitor['left'] + monitor['width'], monitor['top'] + monitor['height']))

    # Iterate over the pixels in the image
    for y in range(0, screenshot.height, 30):
        for x in range(0, screenshot.width, 30):
            # Increment the counter
            counter += 1
            print(f"x: {x}, y: {y}")
            # If the pixel color matches either of the target colors
            if screenshot.getpixel((x, y)) == target_color1 or screenshot.getpixel((x, y)) == target_color2:
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