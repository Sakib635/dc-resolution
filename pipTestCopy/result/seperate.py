import os
import shutil

# Define the source directory containing the txt files
source_directory = 'D:/Windsor/WindsorThesis/Git repo/Thesis-Project-Python-Dependency-Conflict-Resolution/pipTestCopy/pip_packages_log'

# Define the destination directories
non_empty_directory = 'D:/Windsor/WindsorThesis/Git repo/Thesis-Project-Python-Dependency-Conflict-Resolution/pipTestCopy/result/pipSolved'
empty_directory = 'D:/Windsor/WindsorThesis/Git repo/Thesis-Project-Python-Dependency-Conflict-Resolution/pipTestCopy/result/pipUnSolved'

# Create the destination directories if they don't exist
os.makedirs(non_empty_directory, exist_ok=True)
os.makedirs(empty_directory, exist_ok=True)

# Iterate over the files in the source directory
for filename in os.listdir(source_directory):
    if filename.endswith('.txt'):
        file_path = os.path.join(source_directory, filename)
        
        # Check if the file is empty or not
        if os.path.getsize(file_path) > 0:
            # Copy non-empty file to the non_empty_directory
            shutil.copy(file_path, non_empty_directory)
        else:
            # Copy empty file to the empty_directory
            shutil.copy(file_path, empty_directory)

print('Files have been copied successfully.')
