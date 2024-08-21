import webbrowser
import pyautogui
import time

url = 'https://campnet.bits-goa.ac.in:8090/' 

webbrowser.open(url)

time.sleep(0.4)  

pyautogui.click(x=888, y=473)  
pyautogui.write('f20201384')

pyautogui.click(x=882, y=543) 
pyautogui.write('qwerty123')

pyautogui.press('enter')
pyautogui.hotkey('ctrl','w')  