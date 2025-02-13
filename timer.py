import os
import time
import sys

def sendnotif(n=10):
    command = f'notify-send "Timer" "{n} minutes are up"'
    time.sleep(n*60)
    os.system(command)

def main():
    if len(sys.argv) > 1:
        n = int(sys.argv[1])
        sendnotif(n)
    else:
        sendnotif(n=10)

if __name__ == "__main__":
    main()