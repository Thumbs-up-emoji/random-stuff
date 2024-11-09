#deactivate conda before running
import subprocess
import sys

# Define the paths to the two wallpaper images
wallpaper1 = "/home/vk/Pictures/WP/BG3.png"
wallpaper2 = "/home/vk/Pictures/WP/shedinja_by_cariman_d7ei77a-414w-2x.jpg"

def set_wallpaper(wallpaper_path):
    # Command to set the wallpaper (for Cinnamon desktop environment)
    command = f"gsettings set org.cinnamon.desktop.background picture-uri file://{wallpaper_path}"
    subprocess.run(command, shell=True, check=True)

def choose_wallpaper():
    print("Choose a wallpaper:")
    print("1. Wallpaper 1")
    print("2. Wallpaper 2")
    
    choice = input("Enter the number of your choice: ")
    
    if choice == '1':
        set_wallpaper(wallpaper1)
        print("Wallpaper 1 set successfully.")
    elif choice == '2':
        set_wallpaper(wallpaper2)
        print("Wallpaper 2 set successfully.")
    else:
        print("Invalid choice. Please enter 1 or 2.")

def main():
    if len(sys.argv) > 1:
        choice = sys.argv[1]
        if choice == '1':
            set_wallpaper(wallpaper1)
            print("Wallpaper 1 set successfully.")
        elif choice == '2':
            set_wallpaper(wallpaper2)
            print("Wallpaper 2 set successfully.")
        else:
            print("Invalid argument. Please enter 1 or 2.")
    else:
        choose_wallpaper()

if __name__ == "__main__":
    main()