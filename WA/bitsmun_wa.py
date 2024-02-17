import pandas as pd
import pywhatkit as kit
import pyautogui
import time

# Load the Excel file
df = pd.read_excel(r"C:\Users\ASUS\OneDrive - BITS Pilani K K Birla Goa Campus\Desktop\Stuff\CS\random-stuff\new.xlsx")

# Define the message
message = "portfolio"

# Loop through each row in the DataFrame
for index, row in df.iterrows():
    # Access the phone number in the fifth column and convert it to a string
    phone_number = str(row.iloc[4])  # Indices start at 0, so the fifth column is at index 4

    # Send the message
    kit.sendwhatmsg_instantly("+91" + phone_number, message, wait_time=20)
    pyautogui.press("enter")
    time.sleep(20)  # Wait for 20 seconds before sending the next message

print("Successfully Sent!")