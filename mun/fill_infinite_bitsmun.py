import pyautogui
import time
import numpy as np
import random
import keyboard  # Import the keyboard library

def main():
    vector = [(1577, 477), (53, 380), (47, 457), (69, 522), (57, 589), (55, 662), (71, 720), (43, 781), (47, 842), (57, 918)]    

    def fill():
        random_integer = random.randint(1, 5)
        pyautogui.typewrite(str(random_integer))
        pyautogui.press('enter')
        time.sleep(0.4)
        pyautogui.press('enter')
        time.sleep(0.4)

    # Iterate over each element in the vector
    for i in range(1,9):
        # Check if 'esc' key is pressed
        if keyboard.is_pressed('esc'):
            return
        # Click at the location
        pyautogui.click(vector[i])
        time.sleep(0.3)
        pyautogui.click(vector[i])
        time.sleep(4.9)
        pyautogui.click(vector[0])
        time.sleep(0.6)
        pyautogui.click(vector[0])

        # Fill 82 times for each location
        for _ in range(110):
            # Check if 'esc' key is pressed
            if keyboard.is_pressed('esc'):
                return
            fill()

    pyautogui.click(vector[9])

if __name__ == "__main__":
    pyautogui.hotkey('alt', 'tab')
    # Wait for 1 second
    time.sleep(0.4)
    main()