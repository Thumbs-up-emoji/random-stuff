import pyautogui
import time
import numpy as np
import random

vector = np.array([[x0, y0], [x1, y1], [x2, y2], [x3, y3], [x4, y4], [x5, y5], [x6, y6], [x7, y7], [x8, y8], [x9, y9]])

def fill():
    time_value = random.uniform(0.7, 1.7)
    time.sleep(time_value)

    random_integer = random.randint(1, 5)
    pyautogui.typewrite(str(random_integer))
    pyautogui.press('enter')
    pyautogui.press('enter')
    time.sleep(1)

# Iterate over each element in the vector
for location in vector[1:9]:
    # Click at the location
    pyautogui.click(location[0])

    # Fill 82 times for each location
    for _ in range(82):
        fill()

pyautogui.click(vector[9])

