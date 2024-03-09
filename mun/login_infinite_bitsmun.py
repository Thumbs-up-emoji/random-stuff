import pyautogui
import time
import numpy as np
from mss import mss
import keyboard  # Import the keyboard library
from excel_read import read

def main(details):
    time.sleep(0.5)
    # Define the coordinates of the locations
    locations = [(549, 498), (531, 570), (531, 650), (543, 706), (531, 530), (531, 588), (419, 666), (893, 341), (941, 449), (961, 538), (1007, 624), (866, 711), (976, 775), (1274, 1005)]
    # Loop over the first three locations
    for i in range(3):
        # Check if 'esc' key is pressed
        if keyboard.is_pressed('esc'):
            return
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
        # Check if 'esc' key is pressed
        if keyboard.is_pressed('esc'):
            return
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
        # Check if 'esc' key is pressed
        if keyboard.is_pressed('esc'):
            return
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
        # Check if 'esc' key is pressed
        if keyboard.is_pressed('esc'):
            return
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
        # Check if 'esc' key is pressed
        if keyboard.is_pressed('esc'):
            return
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
        # Check if 'esc' key is pressed
        if keyboard.is_pressed('esc'):
            return
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
        # Check if 'esc' key is pressed
        if keyboard.is_pressed('esc'):
            return
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
    main(read()[0])