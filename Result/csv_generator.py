import csv
import re

# Define the input and output file paths
input_file_path = 'D:/Windsor/WindsorThesis/Git repo/Thesis-Project-Python-Dependency-Conflict-Resolution/Result/gist_execution_log.txt'
output_csv_path = 'D:/Windsor/WindsorThesis/Git repo/Thesis-Project-Python-Dependency-Conflict-Resolution/Result/gist_execution_log_processed.csv'

# Define the column names
columns = [
    "Processing file",
    "Reading requirements file execution time",
    "Parsing requirements execution time",
    "Fetching versions and dependencies execution time",
    "Fetching transitive dependencies execution time",
    "Processing folder error",
    "Generating SMT expression execution time",
    "Proof for UNSAT execution time",
    "Solving SMT expression execution time",
    "Generating requirements.txt execution time"
]

# Initialize a list to store the rows of data
data = [columns]

# Regular expressions to extract the data
regex_patterns_updated = {
    "Processing file": re.compile(r"Processing file:.*[\\/](.*?)[\s]execution time:"),
    "Reading requirements file execution time": re.compile(r"Reading requirements file execution time:\s*([\d.]+) seconds"),
    "Parsing requirements execution time": re.compile(r"Parsing requirements execution time:\s*([\d.]+) seconds"),
    "Fetching versions and dependencies execution time": re.compile(r"Fetching versions and dependencies execution time:\s*([\d.]+) seconds"),
    "Fetching transitive dependencies execution time": re.compile(r"Fetching transitive dependencies execution time:\s*([\d.]+) seconds"),
    "Processing folder error": re.compile(r"Processing folder error:\s*(.*)"),
    "Generating SMT expression execution time": re.compile(r"Generating SMT expression execution time:\s*([\d.]+) seconds"),
    "Proof for UNSAT execution time": re.compile(r"Proof for UNSAT execution time:\s*([\d.]+) seconds"),
    "Solving SMT expression execution time": re.compile(r"Solving SMT expression execution time:\s*([\d.]+) seconds"),
    "Generating requirements.txt execution time": re.compile(r"Generating requirements.txt execution time:\s*([\d.]+) seconds")
}

# Function to parse a single block of text and extract the data
def parse_block_updated(block):
    row = []
    for column in columns:
        match = regex_patterns_updated[column].search(block)
        if match:
            row.append(match.group(1))
        else:
            row.append("")
    return row

# Read the input file and parse the data
with open(input_file_path, 'r') as file:
    content = file.read()
    blocks = content.split("Processing file:")
    for block in blocks[1:]:
        block = "Processing file:" + block  # Add back the removed part for consistent parsing
        row = parse_block_updated(block)
        data.append(row)

# Write the data to a CSV file
with open(output_csv_path, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerows(data)

output_csv_path
