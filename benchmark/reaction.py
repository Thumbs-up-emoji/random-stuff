from PIL import ImageGrab
import pyautogui

# Define the pixel to monitor
bbox = (200, 500, 201, 501)

while True:
    # Capture the pixel
    img = ImageGrab.grab(bbox=bbox)
    # print(img.getpixel((0, 0))) debugging line
    # Check the pixel
    if img.getpixel((0, 0)) == (75, 219, 106): # colour in bgr
        # Click without moving the mouse
        print("Green!")
        pyautogui.click()
        break