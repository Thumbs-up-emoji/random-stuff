import pytesseract
import pyautogui
from mss import mss
import cv2
import numpy as np  
import re

pyautogui.FAILSAFE = True

# Specify the path to the Tesseract executable
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Flag variable to indicate whether to stop the program
stop_program = False

# Capture the screen or a part of it
with mss() as sct:
    region = {'top': 470, 'left': 40, 'width': 860, 'height': 250}
    image = sct.grab(region)
    
    # Convert the image to grayscale for accuracy
    image = cv2.cvtColor(np.array(image), cv2.COLOR_RGBA2GRAY)

text = pytesseract.image_to_string(image, config="-c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz,!-:;.`\ ")
text = text.replace("`", "'") # to try and handle apostrophes

# make contraction dictionary with {dont:don't} etc and replace each contraction with each replacement manually

# Replace newline characters with spaces
text = text.replace('\n', ' ')

with open('output.txt', 'w') as f:
    f.write(text)
pyautogui.click(400,600) # focus

# Replace multiple spaces with a single space
text = re.sub(r'\s+', ' ', text)
# Remove trailing whitespaces
text = text.rstrip()

# Use pyautogui to type the extracted text
pyautogui.typewrite(text)