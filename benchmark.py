#L accuracy sadly
import pytesseract
from PIL import ImageGrab
import time
import keyboard
import pyperclip

# Specify the path to the Tesseract executable
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Flag variable to indicate whether to stop the program
stop_program = False

while True:
    # Capture the screen or a part of it
    image = ImageGrab.grab(bbox=(100, 440, 800, 570))

    # Read the text from the image
    text = pytesseract.image_to_string(image)

    #copy text to clipboard
    pyperclip.copy(text)

    # Print the text
    print(text)

    # Start a separate loop to count down from 6 to 1
    for i in range(3, 0, -1):
        # Print the remaining time before the next loop
        print(f"Time before next loop: {i} seconds")

        # Check if 'q' and 'x' are pressed
        if keyboard.is_pressed('esc'):
            print("Stopping program.")
            stop_program = True
            break

        # Pause the program for 1 second
        time.sleep(1)

    # Check the flag variable outside the inner loop
    if stop_program:
        break