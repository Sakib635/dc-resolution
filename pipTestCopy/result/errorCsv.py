import os
import csv

# Define directories
error_log_dir = 'D:/Windsor/WindsorThesis/Git repo/Thesis-Project-Python-Dependency-Conflict-Resolution/pipTestCopy/pip_output_log'
csv_file = 'D:/Windsor/WindsorThesis/Git repo/Thesis-Project-Python-Dependency-Conflict-Resolution/pipTestCopy/result/error_log_summary.csv'

# Function to extract error messages from a log file
def extract_error_messages(log_file):
    error_messages = []
    with open(log_file, 'r') as file:
        for line in file:
            if 'error' in line.lower():
                error_messages.append(line.strip())
    return error_messages

# Create a list to hold the data for the CSV file
error_data = []

# Iterate over each file in the error log directory
for log_file in os.listdir(error_log_dir):
    log_file_path = os.path.join(error_log_dir, log_file)
    if os.path.isfile(log_file_path):
        errors = extract_error_messages(log_file_path)
        if errors:
            error_data.append([log_file, '\n'.join(errors)])

# Write the error data to a CSV file
with open(csv_file, 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Filename', 'Error Messages'])
    writer.writerows(error_data)

print("CSV file created successfully.")