import pyautogui

while True:
# Get the current mouse position
    x, y = pyautogui.position()
    print(f"The current mouse position is {x}, {y}")

