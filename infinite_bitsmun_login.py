import pyautogui
import time
import numpy as np
from mss import mss

# Define the coordinates of the locations
locations = [(x0, y0), (x1, y1), (x2, y2), (x3, y3), (x4, y4), (x5, y5), (x6, y6), (x7, y7), (x8, y8), (x9, y9), (x10, y10), (x11, y11), (x12, y12), (x13, y13), (x14,y14)]

# Define the details to enter at each location
details = ["detail0", "detail1", "detail2", "detail1", "detail2", "detail3", "detail4", "detail5", "detail6", "detail7"]

# Press the Alt+Tab keys
pyautogui.hotkey('alt', 'tab')

# Wait for 1 second
time.sleep(1)

# Loop over the first three locations
for i in range(3):
    # Move the mouse to the location
    pyautogui.click(locations[i])
    time.sleep(1)  # Wait for 1 second

    # Type the detail
    pyautogui.typewrite(details[i])
    time.sleep(1)  # Wait for 1 second

# Take an initial screenshot
with mss() as sct:
    screenshot = sct.grab(sct.monitors[0])

# Loop until the screen changes
while True:
    # Click the fourth location
    pyautogui.click(locations[3])
    time.sleep(1)  # Wait for 1 second

    # Take a new screenshot
    with mss() as sct:
        new_screenshot = sct.grab(sct.monitors[0])

    # Check if the screen has changed
    if not np.array_equal(screenshot, new_screenshot):
        break  # Exit the loop if the screen has changed

# Loop over the fifth and sixth locations
for i in range(4,6):
    # Move the mouse to the location
    pyautogui.click(locations[i])
    time.sleep(1)  # Wait for 1 second

    # Type the detail
    pyautogui.typewrite(details[i])
    time.sleep(1)  # Wait for 1 second

# Take another screenshot
with mss() as sct:
    screenshot = sct.grab(sct.monitors[0])

# Loop until the screen changes
while True:
    # Click the seventh location
    pyautogui.click(locations[6])
    time.sleep(1)  # Wait for 1 second

    # Take a new screenshot
    with mss() as sct:
        new_screenshot = sct.grab(sct.monitors[0])

    # Check if the screen has changed
    if not np.array_equal(screenshot, new_screenshot):
        break  # Exit the loop if the screen has changed

# Loop over the five newest locations
for i in range(8, 13):
    # Move the mouse to the location
    pyautogui.click(locations[i])
    time.sleep(1)  # Wait for 1 second

    # Type the detail
    pyautogui.typewrite(details[i-3])
    time.sleep(1)  # Wait for 1 second

# Take another screenshot
with mss() as sct:
    screenshot = sct.grab(sct.monitors[0])

# Loop until the screen changes
while True:
    # Click the next location
    pyautogui.click(locations[13])
    time.sleep(1)  # Wait for 1 second

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
    pyautogui.click(locations[14])
    time.sleep(1)  # Wait for 1 second

    # Take a new screenshot
    with mss() as sct:
        new_screenshot = sct.grab(sct.monitors[0])

    # Check if the screen has changed
    if not np.array_equal(screenshot, new_screenshot):
        break  # Exit the loop if the screen has changed