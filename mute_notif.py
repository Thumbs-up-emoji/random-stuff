import subprocess
import sys
import os
import re

def get_event_sound_streams():
    """
    Parses pactl output to find sink-inputs with the 'event' media role.
    Returns a list of their indices.
    """
    try:
        result = subprocess.run(["pactl", "list", "sink-inputs"], check=True, capture_output=True, text=True)
    except (FileNotFoundError, subprocess.CalledProcessError):
        return [] # pactl not found or no streams active

    streams = []
    current_index = None
    
    # Regex to find the index of a sink input
    index_re = re.compile(r"Sink Input #(\d+)")
    # Regex to find the media role property
    role_re = re.compile(r"media\.role = \"event\"")

    for line in result.stdout.splitlines():
        index_match = index_re.match(line)
        if index_match:
            current_index = index_match.group(1)
            continue
        
        if current_index and role_re.search(line):
            streams.append(current_index)
            current_index = None # Move to the next sink input block
            
    return streams

def set_event_streams_mute_state(mute):
    """
    Mutes or unmutes all sink-inputs identified as 'event' sounds.
    """
    action = "1" if mute else "0"
    action_str = "Muting" if mute else "Unmuting"
    
    event_streams = get_event_sound_streams()
    
    if not event_streams:
        print("No event sound streams found to modify.")
        return

    print(f"{action_str} {len(event_streams)} event sound stream(s): {', '.join(event_streams)}")
    for stream_index in event_streams:
        try:
            subprocess.run(["pactl", "set-sink-input-mute", stream_index, action], check=True, capture_output=True)
        except subprocess.CalledProcessError as e:
            # This can happen if the stream disappears between listing and muting
            print(f"Could not modify stream {stream_index}: {e.stderr.decode().strip()}", file=sys.stderr)

def main():
    """
    Listens for screen lock/unlock signals and mutes/unmutes event sounds.
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
                set_event_streams_mute_state(True)
            # The line indicating the screen is unlocked contains "boolean false"
            elif "boolean false" in line:
                print("Screen unlocked.")
                set_event_streams_mute_state(False)

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