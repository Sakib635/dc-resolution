import subprocess
import time
import os

# Define the directory containing the requirements files
requirements_dir = 'D:/Windsor/WindsorThesis/Git repo/Thesis-Project-Python-Dependency-Conflict-Resolution/pipTest/watchman'

# Define the output directories
output_dir = 'D:/Windsor/WindsorThesis/Git repo/Thesis-Project-Python-Dependency-Conflict-Resolution/pipTest/pip_output_log'
time_dir = 'D:/Windsor/WindsorThesis/Git repo/Thesis-Project-Python-Dependency-Conflict-Resolution/pipTest/pip_time_log'
packages_dir = 'D:/Windsor/WindsorThesis/Git repo/Thesis-Project-Python-Dependency-Conflict-Resolution/pipTest/pip_packages_log'

# Ensure the output directories exist
os.makedirs(output_dir, exist_ok=True)
os.makedirs(time_dir, exist_ok=True)
os.makedirs(packages_dir, exist_ok=True)

# Function to run a command and capture its output
def run_command(command):
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    return stdout.decode(), stderr.decode()

# Get a list of all requirements files in the directory
requirements_files = [f for f in os.listdir(requirements_dir) if f.startswith('requirements.') and f.endswith('.txt')]

# Process each requirements file
for req_file in requirements_files:
    project_name = req_file.split('.')[1]
    requirements_path = os.path.join(requirements_dir, req_file)
    
    # Define the output file paths
    output_log = os.path.join(output_dir, f'pip_output_log.{project_name}.txt')
    time_log = os.path.join(time_dir, f'pip_time_log.{project_name}.txt')
    packages_log = os.path.join(packages_dir, f'pip_packages_log.{project_name}.txt')
    
    # Ensure the requirements.txt file exists
    if not os.path.isfile(requirements_path):
        print(f"The file {requirements_path} does not exist.")
        continue
    
    # Run pip cache purge without logging its output
    purge_command = ['pip', 'cache', 'purge']
    subprocess.run(purge_command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    # Command to run pip
    pip_command = ['pip', 'install', '--dry-run', '-r', requirements_path]
    
    # Start the timer
    start_time = time.time()
    
    # Run the pip command and capture the output
    with open(output_log, 'w') as log_file:
        stdout, stderr = run_command(pip_command)
        log_file.write(stdout)
        log_file.write(stderr)
    
    # End the timer
    end_time = time.time()
    
    # Calculate the elapsed time
    elapsed_time = end_time - start_time
    
    # Log the elapsed time in a different file
    with open(time_log, 'w') as log_file:
        log_file.write(f"Elapsed time: {elapsed_time:.2f} seconds\n")
    
    # Extract the line with "Would install" and write the packages and versions to a new file
    with open(output_log, 'r') as log_file:
        lines = log_file.readlines()
    
    with open(packages_log, 'w') as pkg_log_file:
        for line in lines:
            if line.startswith("Would install"):
                packages = line[len("Would install "):].strip()
                package_list = packages.split()
                for package in package_list:
                    pkg_log_file.write(package + '\n')
                break
    
    print(f"Processed {req_file}")
    print(f"Pip command output has been logged in {output_log}")
    print(f"Elapsed time has been logged in {time_log}")
    print(f"Packages to be installed have been logged in {packages_log}")
