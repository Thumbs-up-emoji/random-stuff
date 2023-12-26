from youtube_search import YoutubeSearch
import webbrowser
import time
from PIL import ImageGrab , Image
import keyboard
import pyautogui
import numpy as np
from skimage.metrics import structural_similarity as ssim

def vid_over(frame):
    image_path="C:\\Users\\ASUS\\Downloads\\Screenshot (203).png"
    pre_image = np.array(Image.open(image_path).convert("RGB")) #37 x 41 x 3
    # Crop the frame
    cframe = frame[1025:1066, 56:93]  # Replace with your values
    # Ensure the images are the same size
    if cframe.shape != pre_image.shape:
        print("Images must be the same size.")
        return False
    else:
        print("Images are the same size.")
    # Compare the two images
    similarity = ssim(cframe, pre_image, multichannel=True)

    # If the similarity is above a certain threshold, consider the images as equal
    if similarity > 0.9:  # You can adjust this threshold as needed
        print("Video over")
        return True
    else:
        return False

def scrape():
    # Get the pose name from the user
    print("Choose a pose:")
    print("1. Tree")
    print("2. Downward Dog")
    choice = input("Enter the number of your choice: ")

    if choice == '1':
        pose_name = "tree"
    elif choice == '2':
        pose_name = "downward dog"
    else:
        print("Invalid choice. Defaulting to 'downward dog'.")
        pose_name = "downward dog"

    #define the search term
    search_term = "Yoga "+ pose_name

    # Get the number of videos from the user
    n = int(input("Enter the number of videos: "))

    # Search for the term on YouTube
    results = YoutubeSearch(search_term, max_results=n).to_dict()

    for video in results:
        url = 'https://www.youtube.com' + video['url_suffix']
        webbrowser.open(url)
        time.sleep(10)  # Wait for the browser window to become active
        
        # Click on the browser window to bring it into focus
        pyautogui.click(x=400, y=550) 

        # Press 'f' for fullscreen
        pyautogui.press('f')
        
        time.sleep(1) # Wait for 1 second for fullscreen to load

        pyautogui.click(x=400, y=550) # play paused video

        for i in range(4):
            pyautogui.hotkey('shift','.') # 2x speed

        i = 0
        while True:
            # Check if the escape key has been pressed
            if keyboard.is_pressed('esc'):
                break
            
            # Capture the screen
            img = ImageGrab.grab()
            
            np_img=np.array(img)

            if(vid_over(np_img)):
                break

            # Save the image as a JPG file
            img.save(f'C:\\Users\\ASUS\\OneDrive - BITS Pilani K K Birla Goa Campus\\Desktop\\Stuff\\CS\\random-stuff\\yoga_pics\\{pose_name}{i}.jpg')

            # Increment the image number
            i += 1

            # Wait for 0.5 seconds
            time.sleep(5)

        # Close the current tab
        pyautogui.hotkey('ctrl', 'w')

scrape()