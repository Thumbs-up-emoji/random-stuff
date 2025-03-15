import os
import time
import sys
import fcntl
import errno
import json
from datetime import datetime

def is_already_running():
    """Check if another instance is already running using file locking"""
    lock_file = os.path.expanduser("~/.timer_lock")
    
    # Create a file descriptor for the lock file
    try:
        lock_file_fd = open(lock_file, 'w')
        
        # Try to acquire an exclusive lock (will fail if another instance has the lock)
        fcntl.flock(lock_file_fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
        
        # Keep the file descriptor open so the lock persists
        return False, lock_file_fd
    except IOError as e:
        # Lock already held by another process
        if e.errno == errno.EACCES or e.errno == errno.EAGAIN:
            return True, None
        # Some other error
        raise

def save_timer_info(minutes):
    """Save timer information to a file"""
    info_file = os.path.expanduser("~/.timer_info")
    end_time = datetime.now().timestamp() + minutes * 60
    
    timer_info = {
        "end_time": end_time,
        "minutes": minutes
    }
    
    with open(info_file, 'w') as f:
        json.dump(timer_info, f)

def sendnotif(n=10):
    save_timer_info(n)
    command = f'notify-send "Timer" "{n} minutes are up"'
    time.sleep(n*60)
    os.system(command)
    
    # Clean up timer info file
    info_file = os.path.expanduser("~/.timer_info")
    try:
        os.remove(info_file)
    except OSError:
        pass

def check_timer():
    """Check if a timer is running and display time left without starting a new one"""
    info_file = os.path.expanduser("~/.timer_info")
    try:
        with open(info_file, 'r') as f:
            timer_info = json.load(f)
            if "end_time" in timer_info:
                time_left = timer_info["end_time"] - datetime.now().timestamp()
                if time_left > 0:
                    minutes_left = int(time_left // 60)
                    seconds_left = int(time_left % 60)
                    print(f"Timer running! Time left: {minutes_left}m {seconds_left}s")
                    return True
                else:
                    print("Timer appears to have ended but wasn't cleaned up")
                    return False
    except (IOError, json.JSONDecodeError):
        print("No timer is currently running")
        return False

def main():
    # Special case for checking timer status
    if len(sys.argv) > 1 and sys.argv[1] == "0":
        check_timer()
        sys.exit(0)
    
    # For starting a new timer, ignore any running timers
    try:
        lock_fd = None  # Initialize to None in case the try block fails
        already_running, lock_fd = is_already_running()
        
        if len(sys.argv) > 1:
            n = int(sys.argv[1])
            sendnotif(n)
        else:
            sendnotif(n=10)
    finally:
        # Release the lock when done
        if lock_fd:
            fcntl.flock(lock_fd, fcntl.LOCK_UN)
            lock_fd.close()
            
        # Clean up timer info file
        info_file = os.path.expanduser("~/.timer_info")
        try:
            os.remove(info_file)
        except OSError:
            pass
            
if __name__ == "__main__":
    main()