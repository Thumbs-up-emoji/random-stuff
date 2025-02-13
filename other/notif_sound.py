#!/usr/bin/env python3
import subprocess
import sys

class NotificationController:
    def __init__(self):
        # Check if running on Linux
        if sys.platform != 'linux':
            raise OSError("This script is intended for Linux systems only")
    
    def get_sound_state(self):
        """Get current state of notification sounds"""
        try:
            result = subprocess.run(
                ['gsettings', 'get', 'org.cinnamon.sounds', 'notification-enabled'],
                capture_output=True,
                text=True,
                check=True
            )
            return result.stdout.strip() == 'true'
        except subprocess.CalledProcessError as e:
            print(f"Error getting notification sound state: {e}")
            return None
            
    def disable_notification_sounds(self):
        """Disable notification sounds in Linux Mint"""
        try:
            subprocess.run(['gsettings', 'set', 'org.cinnamon.sounds', 'notification-enabled', 'false'], 
                         check=True)
            print("Notification sounds have been disabled")
            return True
        except subprocess.CalledProcessError as e:
            print(f"Error disabling notification sounds: {e}")
            return False
            
    def enable_notification_sounds(self):
        """Enable notification sounds in Linux Mint"""
        try:
            subprocess.run(['gsettings', 'set', 'org.cinnamon.sounds', 'notification-enabled', 'true'], 
                         check=True)
            print("Notification sounds have been enabled")
            return True
        except subprocess.CalledProcessError as e:
            print(f"Error enabling notification sounds: {e}")
            return False
    
    def toggle_notification_sounds(self):
        """Toggle notification sounds on/off"""
        current_state = self.get_sound_state()
        if current_state is None:
            print("Could not determine current notification sound state")
            return False
            
        if current_state:
            return self.disable_notification_sounds()
        else:
            return self.enable_notification_sounds()
            
    def disable_all_notifications(self):
        """Disable all notifications in Linux Mint"""
        try:
            subprocess.run(['gsettings', 'set', 'org.cinnamon.desktop.notifications', 'display-notifications', 'false'], 
                         check=True)
            print("All notifications have been disabled")
            return True
        except subprocess.CalledProcessError as e:
            print(f"Error disabling notifications: {e}")
            return False
            
    def enable_all_notifications(self):
        """Enable all notifications in Linux Mint"""
        try:
            subprocess.run(['gsettings', 'set', 'org.cinnamon.desktop.notifications', 'display-notifications', 'true'], 
                         check=True)
            print("All notifications have been enabled")
            return True
        except subprocess.CalledProcessError as e:
            print(f"Error enabling notifications: {e}")
            return False

if __name__ == "__main__":
    controller = NotificationController()
    # Toggle notification sounds
    controller.toggle_notification_sounds()
