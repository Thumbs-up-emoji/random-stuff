import webbrowser
import pyautogui
import time

pyautogui.hotkey('alt', 'tab')
    # Wait for 1 second
time.sleep(0.4)

pyautogui.hotkey('ctrl', 'w')

    # Open a new tab with a specific URL
webbrowser.open('https://umm-scoring-external-full.infiniteanalytics.com/register', new=2)
