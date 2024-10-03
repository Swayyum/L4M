import os
import hashlib

# Define the paths to your data (adjust accordingly)
man_pages_path = "D:/LLLM Data/linux_data/man_pages"
syscalls_path = "D:/LLLM Data/linux_data/syscalls"
github_scripts_path = "D:/LLLM Data/linux_data/github_shell_scripts"

# Define a function to shorten file names
def shorten_filename(original_name, max_length=10):
    # Create a short hash based on the original name to ensure uniqueness
    short_hash = hashlib.md5(original_name.encode('utf-8')).hexdigest()[:max_length]
    return short_hash

# Define a function to rename files in a folder
def rename_files_in_folder(folder_path, valid_extensions=(".txt", ".sh")):
    counter = 1
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith(valid_extensions):
                original_file_path = os.path.join(root, file)

                # Shorten the file name and preserve the extension
                file_extension = os.path.splitext(file)[1]
                short_name = f"file_{counter}{file_extension}"
                
                # Create the new file path with the shortened name
                new_file_path = os.path.join(root, short_name)

                # Rename the file
                os.rename(original_file_path, new_file_path)
                print(f"Renamed: {original_file_path} to {new_file_path}")

                counter += 1

# Rename files in all folders
print("Renaming man pages...")
rename_files_in_folder(man_pages_path)

print("Renaming syscalls...")
rename_files_in_folder(syscalls_path)

print("Renaming GitHub shell scripts...")
rename_files_in_folder(github_scripts_path, valid_extensions=(".sh"))

print("File renaming completed!")
