import os
import re
import json

# Define the paths to your data (adjust according to your directory structure)
man_pages_path = "D:/LLLM Data/linux_data/man_pages"
syscalls_path = "D:/LLLM Data/linux_data/syscalls"
github_scripts_path = "D:/LLLM Data/linux_data/github_shell_scripts"

# Define a function to clean and preprocess each file
def preprocess_text(text):
    # Remove any extraneous control characters or backspaces
    text = re.sub(r'.\x08', '', text)
    
    # Remove extra spaces and newlines
    text = re.sub(r'\s+', ' ', text)
    
    return text.strip()

# Define a function to process a folder recursively
def process_folder(folder_path, valid_extensions=(".txt", ".sh")):
    processed_data = []
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith(valid_extensions):  # Process .txt and .sh files
                # Open and read each file
                with open(os.path.join(root, file), 'r', encoding='utf-8') as f:
                    text = f.read()
                    cleaned_text = preprocess_text(text)
                    
                    # Add to the processed data
                    processed_data.append({
                        "filename": file,
                        "path": os.path.join(root, file),  # Full path to file
                        "content": cleaned_text
                    })
    return processed_data

# Process each folder
print("Processing man pages...")
man_pages_data = process_folder(man_pages_path)

print("Processing syscalls...")
syscalls_data = process_folder(syscalls_path)

print("Processing GitHub shell scripts...")
github_scripts_data = process_folder(github_scripts_path, valid_extensions=(".sh"))  # Only process .sh files

# Combine all data
all_processed_data = {
    "man_pages": man_pages_data,
    "syscalls": syscalls_data,
    "github_shell_scripts": github_scripts_data
}

# Save the processed data to a JSON file for training
with open('processed_linux_data.json', 'w', encoding='utf-8') as out_file:
    json.dump(all_processed_data, out_file, indent=4)

print(f"Processed {len(man_pages_data)} man pages, {len(syscalls_data)} syscalls, and {len(github_scripts_data)} GitHub scripts.")
