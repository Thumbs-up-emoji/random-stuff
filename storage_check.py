import os

def get_folder_size(start_path):
    total_size = 0
    with open('not_found_files.txt', 'a') as file:
        for dirpath, _, filenames in os.walk(start_path):
            for f in filenames:
                fp = os.path.join(dirpath, f)
                try:
                    total_size += os.path.getsize(fp)
                except FileNotFoundError:
                    file.write(f"File not found: {fp}\n")
    return total_size

def get_immediate_subfolder_sizes(start_path):
    folder_sizes = {}
    for item in os.listdir(start_path):
        item_path = os.path.join(start_path, item)
        if os.path.isdir(item_path):
            folder_size = get_folder_size(item_path) / (1024 * 1024)  # size in megabytes
            folder_sizes[item] = folder_size  # store the relative path
    return folder_sizes

# Usage
folder_sizes = get_immediate_subfolder_sizes('C:\\Users\\ASUS\\OneDrive - BITS Pilani K K Birla Goa Campus\\Desktop\\Stuff\\DC')

# Sort the folders by size in descending order
sorted_folder_sizes = sorted(folder_sizes.items(), key=lambda item: item[1], reverse=True)

for folder, size in sorted_folder_sizes:
    print(f'Folder: {folder}, Size: {round(size, 2)} MB')