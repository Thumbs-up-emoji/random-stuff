# has some trouble with 7 vs 1, and sometimes doesn't actually copy to clipboard but good enough for now
# need to try automatic input, hitting ctrl+v every time is good, but not enough
# also can try pytesseract alternatives
# need to try further preprocessing, see bing chat
import cv2
import numpy as np
import pytesseract
from mss import mss
import time
import keyboard
import pyperclip

# Specify the path to the Tesseract executable
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Flag variable to indicate whether to stop the program
stop_program = False

while True:
    # Capture the screen or a part of it
    with mss() as sct:
        region = {'top': 450, 'left': 0, 'width': 900, 'height': 580}
        image = sct.grab(region)
    
    # Convert the image to grayscale
    image = cv2.cvtColor(np.array(image), cv2.COLOR_RGBA2GRAY)

    # Invert the color scheme
    image = cv2.bitwise_not(image)

    # Resize the image
    new_size = (image.shape[1]*2, image.shape[0]*2)  # Double the size
    image = cv2.resize(image, new_size)

    # Apply thresholding to binarize the image
    _, image = cv2.threshold(image, 210, 255, cv2.THRESH_BINARY)

    if keyboard.is_pressed('s'):    
        cv2.imshow('image', image)
        cv2.waitKey(1)

    # Read the text from the image
    text = pytesseract.image_to_string(image, config='--psm 6 outputbase digits')

    # Copy text to clipboard
    if text.strip():
        pyperclip.copy(text)

    # Print the text
    print(text)

    # Start a separate loop to count down from 6 to 1
    for i in range(1, 0, -1):
        # Print the remaining time before the next loop
        print(f"Time before next loop: {i} seconds")

        # Check if 'esc' is pressed
        if keyboard.is_pressed('esc'):
            print("Stopping program.")
            stop_program = True
            break

        # Pause the program for 1 second
        time.sleep(1)

    # Check the flag variable outside the inner loop
    if stop_program:
        cv2.destroyAllWindows()
        break