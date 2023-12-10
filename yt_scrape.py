from youtube_search import YoutubeSearch
import subprocess
import time
from PIL import ImageGrab
import keyboard
import pyautogui

# Get the pose name from the user
print("Choose a pose:")
print("1. Tree")
print("2. Downward Dog")
choice = input("Enter the number of your choice: ")

if choice == '1':
    pose_name = "tree"
    pose_label = pose_name
elif choice == '2':
    pose_name = "downward dog"
    pose_label = "downdog"
else:
    print("Invalid choice. Defaulting to 'downward dog'.")
    pose_name = "downward dog"
    pose_label = "downdog"

#define the search term
search_term = "Yoga "+ pose_name

# Get the number of videos from the user
n = int(input("Enter the number of videos: "))

# Search for the term on YouTube
results = YoutubeSearch(search_term, max_results=n).to_dict()

brave_path = r"C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe" 


for video in results:
    url = 'https://www.youtube.com' + video['url_suffix']
    subprocess.Popen([brave_path, '--incognito', url])
    time.sleep(8)  # Wait for the browser window to become active

    # Click on the browser window to bring it into focus
    pyautogui.click(x=400, y=500)

    # Mute the video
    pyautogui.press('m')

    # Press 'f' for fullscreen
    pyautogui.press('f')
    
    # Wait for 1 seconds for fullscreen to load
    time.sleep(1)

    pyautogui.click(x=400, y=500) # play paused video

    for i in range(4):
        pyautogui.hotkey('shift','.') # 2x speed

    i = 0
    while True:
        # Check if the escape key has been pressed
        if keyboard.is_pressed('esc'):
            break
        # Capture the screen
        img = ImageGrab.grab()
        if img is not None:
            # Save the image as a JPG file
            img.save(f'C:\\Users\\ASUS\\OneDrive - BITS Pilani K K Birla Goa Campus\\Desktop\\Stuff\\CS\\random-stuff\\yoga_pics\\{pose_name}{i}.jpg')

            # Increment the image number
            i += 1

            # Wait for 0.5 seconds
            time.sleep(60)

    # Close the current tab
    pyautogui.hotkey('ctrl', 'w')