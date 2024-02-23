import pyautogui
import time
import numpy as np
from mss import mss

def main(details):
    time.sleep(0.5)
    # Define the coordinates of the locations
    locations = [(549, 463), (531, 535), (531, 615), (543, 671), (531, 495), (531, 553), (419, 631), (893, 306), (941, 374), (961, 493), (1007, 589), (866, 666), (976, 740), (1274, 1000)]

    # Loop over the first three locations
    for i in range(3):
        # Move the mouse to the location
        pyautogui.click(locations[i])
        pyautogui.click(locations[i])
        time.sleep(0.4)  # Wait for 1 second

        # Type the detail
        pyautogui.typewrite(details[i])
        time.sleep(0.4)  # Wait for 1 second

    # Take an initial screenshot
    with mss() as sct:
        screenshot = sct.grab(sct.monitors[0])

    # Loop until the screen changes
    while True:
        # Click the fourth location
        pyautogui.click(locations[3])
        pyautogui.click(locations[3])
        time.sleep(0.4)
        pyautogui.click(locations[3])
        pyautogui.click(locations[3])
        time.sleep(0.4)  
        pyautogui.click(locations[3])

        # Take a new screenshot
        with mss() as sct:
            new_screenshot = sct.grab(sct.monitors[0])

        # Check if the screen has changed
        if not np.array_equal(screenshot, new_screenshot):
            break  # Exit the loop if the screen has changed

    for i in range(4,6):
        # Move the mouse to the location
        pyautogui.click(locations[i])
        pyautogui.click(locations[i])
        time.sleep(0.4)  # Wait for 1 second

        # Type the detail
        pyautogui.typewrite(details[i-1])
        time.sleep(0.4)  # Wait for 1 second

    # Take another screenshot
    with mss() as sct:
        screenshot = sct.grab(sct.monitors[0])

    # Loop until the screen changes
    while True:
        # Click the seventh location
        pyautogui.click(locations[6])
        pyautogui.click(locations[6])
        time.sleep(0.4)  # Wait for 1 second

        # Take a new screenshot
        with mss() as sct:
            new_screenshot = sct.grab(sct.monitors[0])

        # Check if the screen has changed
        if not np.array_equal(screenshot, new_screenshot):
            break  # Exit the loop if the screen has changed

    time.sleep(1.2)

    # Loop over the five newest locations
    for i in range(7, 12):
        # Move the mouse to the location
        pyautogui.click(locations[i])
        pyautogui.click(locations[i])
        time.sleep(0.4)  # Wait for 1 second

        # Type the detail
        pyautogui.typewrite(details[i-2])
        time.sleep(0.4)  # Wait for 1 second

    # Take another screenshot
    with mss() as sct:
        screenshot = sct.grab(sct.monitors[0])

    # Loop until the screen changes
    while True:
        # Click the next location
        pyautogui.click(locations[12])
        pyautogui.click(locations[12])
        time.sleep(0.4)  # Wait for 1 second

        # Take a new screenshot
        with mss() as sct:
            new_screenshot = sct.grab(sct.monitors[0])

        # Check if the screen has changed
        if not np.array_equal(screenshot, new_screenshot):
            break  # Exit the loop if the screen has changed

    # Take another screenshot
    with mss() as sct:
        screenshot = sct.grab(sct.monitors[0])

    # Loop until the screen changes
    while True:
        # Click the seventh location
        pyautogui.click(locations[13])
        pyautogui.click(locations[13])
        time.sleep(0.4)  # Wait for 1 second

        # Take a new screenshot
        with mss() as sct:
            new_screenshot = sct.grab(sct.monitors[0])

        # Check if the screen has changed
        if not np.array_equal(screenshot, new_screenshot):
            break  # Exit the loop if the screen has changed

if __name__ == "__main__":
    # Press the Alt+Tab keys     
    pyautogui.hotkey('alt', 'tab')
    # Wait for 1 second
    time.sleep(0.4)
    main()