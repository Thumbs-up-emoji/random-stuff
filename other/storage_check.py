import os
import math
import ctypes

class WIN32_FILE_ATTRIBUTE_DATA(ctypes.Structure):
    _fields_ = [("dwFileAttributes", ctypes.c_ulong),
                ("ftCreationTime", ctypes.c_ulonglong),
                ("ftLastAccessTime", ctypes.c_ulonglong),
                ("ftLastWriteTime", ctypes.c_ulonglong),
                ("nFileSizeHigh", ctypes.c_ulong),
                ("nFileSizeLow", ctypes.c_ulong)]

def get_folder_size(start_path):
    total = 0
    sectors_per_cluster = ctypes.c_ulonglong(0)
    bytes_per_sector = ctypes.c_ulonglong(0)
    ctypes.windll.kernel32.GetDiskFreeSpaceW(start_path, ctypes.byref(sectors_per_cluster), ctypes.byref(bytes_per_sector), None, None)
    block_size = sectors_per_cluster.value * bytes_per_sector.value  # calculate the block size
    FILE_ATTRIBUTE_RECALL_ON_DATA_ACCESS = 0x00400000  # the file attribute for online-only files on OneDrive
    with open('not_found_files.txt', 'a') as file:
        for dirpath, _, filenames in os.walk(start_path):
            for f in filenames:
                fp = os.path.join(dirpath, f)
                try:
                    # create a WIN32_FILE_ATTRIBUTE_DATA structure
                    attrs = WIN32_FILE_ATTRIBUTE_DATA()
                    # get the file attributes
                    ctypes.windll.kernel32.GetFileAttributesExW(fp, 0, ctypes.byref(attrs))
                    # check if the file is online only
                    if attrs.dwFileAttributes & FILE_ATTRIBUTE_RECALL_ON_DATA_ACCESS:
                        continue  # skip this file
                    file_size = os.path.getsize(fp)
                    blocks = math.ceil(file_size / block_size)
                    total += blocks * block_size
                except FileNotFoundError:
                    file.write(f"File not found: {fp}\n")
    return total

def get_immediate_subfolder_sizes(start_path):
    folder_sizes = {}
    for item in os.listdir(start_path):
        item_path = os.path.join(start_path, item)
        if os.path.isdir(item_path):
            folder_size = get_folder_size(item_path) / (1024 * 1024)  # size in megabytes
            folder_sizes[item] = folder_size  # store the relative path
    return folder_sizes

# Usage
folder_sizes = get_immediate_subfolder_sizes('C:\\Users\\ASUS\\OneDrive - BITS Pilani K K Birla Goa Campus\\Desktop\\Stuff')

# Sort the folders by size in descending order
sorted_folder_sizes = sorted(folder_sizes.items(), key=lambda item: item[1], reverse=True)

for folder, size in sorted_folder_sizes:
    print(f'Folder: {folder}, Size: {round(size, 2)} MB')