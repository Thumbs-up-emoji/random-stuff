import webbrowser
import pyautogui
import time
import csv
import sys
import random

def get_login_details(line_num):
    with open('/home/vk/CS/random-stuff/login_details.csv', newline='') as csvfile:
        reader = csv.reader(csvfile)
        for idx, row in enumerate(reader, start=1):
            if idx == line_num:
                return row[0], row[1]
    raise ValueError("Line number out of range in login_details.csv")

if len(sys.argv) < 2:
    line_number = random.randint(1, 9)
    print(f"No line number provided. Using random line: {line_number}")
else:
    line_number = int(sys.argv[1])

username, password = get_login_details(line_number)

url = 'https://campnet.bits-goa.ac.in:8090/' 
webbrowser.open(url)
time.sleep(1)  

pyautogui.click(x=1037, y=367)  
pyautogui.write(username)

pyautogui.click(x=1044, y=432) 
pyautogui.write(password)

pyautogui.press('enter')
pyautogui.hotkey('ctrl','w')  
pyautogui.hotkey('alt','tab')
pyautogui.hotkey('alt','q')  
pyautogui.press('enter')