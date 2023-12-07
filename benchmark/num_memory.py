# need to press enter automatically
# need to try further preprocessing to solve accuracy issues, see brave bookmarks
# else could look into tesseract alternatives
# worst case, could try to train tesseract to recognize the font
import cv2
import numpy as np
import pytesseract
from mss import mss
import time
import keyboard
import pyautogui
import re

pyautogui.FAILSAFE = True

# Specify the path to the Tesseract executable
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Flag variable to indicate whether to stop the program
stop_program = False

while True:
    # Capture the screen or a part of it
    with mss() as sct:
        region = {'top': 450, 'left': 0, 'width': 900, 'height': 130}
        image = sct.grab(region)
    
    # Convert the image to grayscale
    image = cv2.cvtColor(np.array(image), cv2.COLOR_RGBA2GRAY)

    # Invert the color scheme
    #image = cv2.bitwise_not(image)

    # Resize the image
    #new_size = (image.shape[1]*2, image.shape[0]*2)  # Double the size
    #image = cv2.resize(image, new_size)

    # Apply thresholding to binarize the image
    #_, image = cv2.threshold(image, 210, 255, cv2.THRESH_BINARY)

    if keyboard.is_pressed('s'): 
        cv2.destroyAllWindows() # close previous window   
        cv2.imshow('image', image)
        cv2.waitKey(0)

    # Read the text from the image
    text = pytesseract.image_to_string(image, config='--psm 6 outputbase digits')

    # Extract only the digits from the text
    digits_text = ''.join(re.findall('\d+', text))

    if digits_text:  
    # Move the mouse to the desired location (x, y)
        pyautogui.moveTo(500, 450)  # replace 100, 200 with your desired coordinates

        # Click the mouse
        pyautogui.click()

        time.sleep(0.5)

        # Type the text
        pyautogui.write(digits_text)
        #pyautogui.press('enter')

        #time.sleep(0.5)

        #pyautogui.press('enter')
    # Print the text
    print(text)

    #countdown
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
        break