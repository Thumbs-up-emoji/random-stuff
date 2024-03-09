import login_infinite_bitsmun
import fill_infinite_bitsmun
import pyautogui
import time
import webbrowser
from excel_read import read

details_list = read()

def main(details):
    time.sleep(1)
    # Close the current tab

    # Open a new tab with a specific URL
    webbrowser.open('https://umm-scoring-external-full.infiniteanalytics.com/register', new=2)
    time.sleep(1)
    login_infinite_bitsmun.main(details)
    fill_infinite_bitsmun.main()

#for i in range(2):
    # Get the ith sublist
    #details = details_list[i]
    #details[9]="0"
    #main(details)

if __name__ == "__main__":
# Press the Alt+Tab keys         
    pyautogui.hotkey('alt', 'tab')
    # Wait for 1 second
    time.sleep(0.4)
    for i in range(25):    
        details = details_list[1]
        details[9]="0"
        main(details)