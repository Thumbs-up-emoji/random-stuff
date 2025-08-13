@echo off
REM Script to mount physical drive in WSL and navigate to specific directory

REM Step 1: Launch PowerShell as admin and execute WSL mount command
REM Step 2: Mount the physical drive (replace # with your actual drive number)
echo Mounting physical drive in WSL...
powershell -Command "Start-Process powershell -ArgumentList '-Command wsl --mount \\.\PHYSICALDRIVE0 --bare' -Verb RunAs -Wait"

REM Wait a moment for the mount to complete
timeout /t 3 /nobreak >nul

REM Step 3: Create mount directory
echo Creating mount directory...
wsl mkdir -p /mnt/my-linux

REM Step 4: Mount the ext4 partition
echo Mounting ext4 partition...
wsl sudo mount -t ext4 /dev/sdd5 /mnt/my-linux

REM Step 5: Navigate to target directory and start interactive shell
echo Navigating to target directory...
wsl bash -c "cd /mnt/my-linux/home/vk && bash"

echo Script completed.
pause