import webbrowser
import pyautogui
import time

url = 'https://campnet.bits-goa.ac.in:8090/' 

webbrowser.open(url)

time.sleep(1)  

pyautogui.click(x=969, y=496)  
pyautogui.write('f20201384')

pyautogui.click(x=963, y=568) 
pyautogui.write('qwerty123')

pyautogui.press('enter')
pyautogui.hotkey('ctrl','w')  