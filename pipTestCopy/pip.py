import subprocess
import time
import os

# Define the paths
requirements_path = 'D:/Windsor/WindsorThesis/Git repo/Thesis-Project-Python-Dependency-Conflict-Resolution/pipTest/r.txt'
output_log = 'D:/Windsor/WindsorThesis/Git repo/Thesis-Project-Python-Dependency-Conflict-Resolution/pipTest/result/pip_output_log.txt'
time_log = 'D:/Windsor/WindsorThesis/Git repo/Thesis-Project-Python-Dependency-Conflict-Resolution/pipTest/result/pip_time_log.txt'
packages_log = 'D:/Windsor/WindsorThesis/Git repo/Thesis-Project-Python-Dependency-Conflict-Resolution/pipTest/result/pip_packages_log.txt'

# Ensure the requirements.txt file exists
if not os.path.isfile(requirements_path):
    print(f"The file {requirements_path} does not exist.")
    exit(1)

# Function to run a command and capture its output
def run_command(command):
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    return stdout.decode(), stderr.decode()

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

    # Log the output
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

print(f"Pip command output has been logged in {output_log}")
print(f"Elapsed time has been logged in {time_log}")
print(f"Packages to be installed have been logged in {packages_log}")
