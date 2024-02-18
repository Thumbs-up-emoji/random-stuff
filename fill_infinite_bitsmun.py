import pyautogui
import time
import numpy as np
import random

def main():
    vector = [(1477, 427), (53, 360), (47, 437), (69, 502), (57, 569), (55, 642), (71, 700), (43, 761), (47, 822), (57, 888)]    

    def fill():
        random_integer = random.randint(1, 5)
        pyautogui.typewrite(str(random_integer))
        pyautogui.press('enter')
        time.sleep(0.5)
        pyautogui.press('enter')
        time.sleep(0.5)

    # Iterate over each element in the vector
    for i in range(1,10):
        # Click at the location
        pyautogui.click(vector[i])
        time.sleep(0.1)
        pyautogui.click(vector[i])
        time.sleep(0.8)
        pyautogui.click(vector[0])
        time.sleep(0.1)
        pyautogui.click(vector[0])

        # Fill 82 times for each location
        for _ in range(90):
            fill()

    pyautogui.click(vector[9])

if __name__ == "__main__":
    pyautogui.hotkey('alt', 'tab')
    # Wait for 1 second
    time.sleep(0.4)
    main()