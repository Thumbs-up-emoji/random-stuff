import subprocess
import sys
import os

def set_mute_state(mute):
    """
    Mutes or unmutes the default audio sink using pactl.
    :param mute: True to mute, False to unmute.
    """
    action = "1" if mute else "0"
    action_str = "Muting" if mute else "Unmuting"
    print(f"{action_str} system audio.")
    try:
        # Use @DEFAULT_SINK@ to target the current default sink
        subprocess.run(["pactl", "set-sink-mute", "@DEFAULT_SINK@", action], check=True, capture_output=True)
    except FileNotFoundError:
        print("Error: 'pactl' command not found. Please install 'pulseaudio-utils'.", file=sys.stderr)
        sys.exit(1)
    except subprocess.CalledProcessError as e:
        print(f"Error executing pactl: {e.stderr.decode().strip()}", file=sys.stderr)
        # Don't exit, as this might be a temporary issue (e.g., no audio device)
        
def main():
    """
    Listens for screen lock/unlock signals using dbus-monitor and mutes/unmutes audio.
    """
    # Ensure we're in a graphical session
    if not os.environ.get('DISPLAY'):
        print("Error: This script must be run in a graphical session.", file=sys.stderr)
        sys.exit(1)

    # Command to monitor the Cinnamon screensaver signal
    # This works for Linux Mint Cinnamon. Other desktop environments might use a different interface.
    # e.g., MATE: org.mate.ScreenSaver, GNOME: org.gnome.ScreenSaver
    monitor_command = [
        "dbus-monitor",
        "--session",
        "type='signal',interface='org.cinnamon.ScreenSaver',member='ActiveChanged'"
    ]

    process = None
    try:
        print("Starting dbus-monitor to listen for screen lock events...")
        process = subprocess.Popen(monitor_command, stdout=subprocess.PIPE, text=True, bufsize=1)

        # Ensure stdout pipe is available and read the output line by line
        if process.stdout is None:
            raise RuntimeError("Failed to capture dbus-monitor stdout.")
        for line in iter(process.stdout.readline, ''):
            line = line.strip()
            # The line indicating the screen is locked contains "boolean true"
            if "boolean true" in line:
                print("Screen locked.")
                set_mute_state(True)
            # The line indicating the screen is unlocked contains "boolean false"
            elif "boolean false" in line:
                print("Screen unlocked.")
                set_mute_state(False)

    except FileNotFoundError:
        print("Error: 'dbus-monitor' command not found. Please ensure 'dbus' is installed.", file=sys.stderr)
        sys.exit(1)
    except KeyboardInterrupt:
        print("\nScript stopped by user.")
    finally:
        if process:
            process.terminate()
            process.wait()
        print("dbus-monitor stopped.")

if __name__ == "__main__":
    main()