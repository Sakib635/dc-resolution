import os
from process import process_folder, read_json_file

def main():
    base_directory = 'D:/Windsor/WindsorThesis/Git repo/Thesis-Project-Python-Dependency-Conflict-Resolution/Dataset/watchman'
    # base_directory = 'D:/Windsor/WindsorThesis/Git repo/Thesis-Project-Python-Dependency-Conflict-Resolution/Dataset/hard-gists-reqs'
    projects_data_filepath = 'D:/Windsor/WindsorThesis/Git repo/Thesis-Project-Python-Dependency-Conflict-Resolution/Dataset/KGBase10k.json'

    # Read the projects data once
    try:
        projects_data = read_json_file(projects_data_filepath)
    except Exception as e:
        print(f"Error reading projects data: {e}")
        return

    # Get all folders in the base directory
    try:
        folders = [folder for folder in os.listdir(base_directory) if os.path.isdir(os.path.join(base_directory, folder))]
    except Exception as e:
        print(f"Error listing folders in base directory: {e}")
        return

    # Process each folder
    for folder in folders:
        process_folder(os.path.join(base_directory, folder), projects_data)

if __name__ == "__main__":
    main()
