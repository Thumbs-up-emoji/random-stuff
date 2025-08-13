import sys
import subprocess
import os

def main():
    if len(sys.argv) > 2:
        print("Usage: python merge.py [1|2]")
        print("  (default is 1)")
        print("  1: Run trump.py")
        print("  2: Run tweet.py")
        sys.exit(1)

    # Default to '1' if no argument is provided
    choice = sys.argv[1] if len(sys.argv) == 2 else '1'
    script_dir = os.path.dirname(__file__)

    if choice == '1':
        script_to_run = os.path.join(script_dir, 'trump.py')
        print(f"Running {script_to_run}...")
        subprocess.run(['python', script_to_run])
    elif choice == '2':
        script_to_run = os.path.join(script_dir, 'tweet.py')
        print(f"Running {script_to_run}...")
        subprocess.run(['python', script_to_run])
    else:
        print("Invalid argument. Please use 1 or 2.")
        sys.exit(1)

if __name__ == "__main__":
    main()