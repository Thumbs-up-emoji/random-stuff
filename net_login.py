import webbrowser
import pyautogui
import time

url = 'https://campnet.bits-goa.ac.in:8090/' 

webbrowser.open(url)

time.sleep(1)  

pyautogui.click(x=900, y=450)  
pyautogui.write('f20221197')

pyautogui.click(x=900, y=520) 
pyautogui.write('What_If317')

pyautogui.press('enter')
pyautogui.hotkey('ctrl','w')  
pyautogui.hotkey('alt','tab')
pyautogui.hotkey('alt','q')  
pyautogui.press('enter')