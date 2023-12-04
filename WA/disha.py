# importing the module
import pywhatkit
import pyautogui
import time

# using Exception Handling to avoid 
# unprecedented errors
try:

# sending message to receiver
# using pywhatkit
	pywhatkit.sendwhatmsg_instantly("+918008602198", "hello and namaste today", wait_time=85)

	pyautogui.press("enter")	

	print("Successfully Sent!")

except:

# handling exception 
# and printing error message
	print("An Unexpected Error!")
