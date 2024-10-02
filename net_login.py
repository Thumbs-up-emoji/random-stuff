import webbrowser
import pyautogui
import time

url = 'https://campnet.bits-goa.ac.in:8090/' 

webbrowser.open(url)

time.sleep(1)  

pyautogui.click(x=1200, y=496)  
pyautogui.write('f20221197')

pyautogui.click(x=1200, y=568) 
pyautogui.write('What_If317')

pyautogui.press('enter')
pyautogui.hotkey('ctrl','w')  