#automate this task
#make separate one with bits/stdc++.h
import pyautogui
import time

time.sleep(5)  # Wait for 5 seconds to switch to the target application

pyautogui.write("#include<iostream>\n", interval=0.1)
pyautogui.write("using namespace std;\n", interval=0.1)
pyautogui.write("int main()\n", interval=0.1)
pyautogui.write("{\n", interval=0.1)
pyautogui.write("return 0;\n", interval=0.1)
pyautogui.write("}", interval=0.1)