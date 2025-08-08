#!/bin/bash

# The MAC address of your Bluetooth headphones
DEVICE_MAC="80:C3:BA:6F:1A:EB"

# Function to check if the device is connected
check_connection() {
    if bluetoothctl info "$DEVICE_MAC" | grep -q "Connected: yes"; then
        return 0
    else
        return 1
    fi
}

# Unblock Bluetooth using rfkill
rfkill unblock bluetooth

# Ensure the Bluetooth adapter is powered on
bluetoothctl power on

# Wait for 0.5 seconds to ensure the adapter is powered on
sleep 0.5

# Check if the device is already connected
if check_connection; then
    echo "Device is already connected."
    exit 0
fi

# Attempt to connect to the device
echo "Attempting to connect to the device..."
bluetoothctl connect "$DEVICE_MAC"

# Check if the connection was successful
if check_connection; then
    echo "Successfully connected to the device."
    exit 0
else
    echo "Failed to connect to the device."
    exit 1
fi