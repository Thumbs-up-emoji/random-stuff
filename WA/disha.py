# importing the module
import pywhatkit
import pyautogui

# sending message to receiver
# using pywhatkit

pywhatkit.sendwhatmsg_instantly("+918008602198", "hello and namaste today", wait_time=5)
pyautogui.press("enter")	
print("Successfully Sent!")

