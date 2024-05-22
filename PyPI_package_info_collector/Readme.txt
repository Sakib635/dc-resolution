# PyPI_Package_Info_Collector
This script fetches information about Python packages from the PyPI repository, processes each package to retrieve details about its versions and dependencies, and stores this information in a JSON file. Additionally, it handles errors gracefully and logs any packages that could not be processed to a separate JSON file.

Here’s a detailed breakdown of what the script does:

 Main Features of the Script:

1. Fetch Package Versions:
   - For each package, the script fetches a list of all its versions from PyPI.

2. Fetch Package Information:
   - For each version of each package, the script retrieves detailed information, including the package name, version, dependencies, and required Python version.

3. Error Handling:
   - If an error occurs while fetching information for any package, the script does not stop execution. Instead, it logs the package name in a separate list of failed packages.

4. Logging and JSON File Updates:
   - The script periodically updates a JSON file (`all_package_info.json`) with the collected package information and another JSON file (`failed_packages.json`) with the names of packages that failed to download.
   - It updates these JSON files every minute and once more at the end of the execution.

5. Command-Line Argument Parsing:
   - The script uses the `argparse` module to accept the path to a JSON file containing a list of packages as a command-line argument. This allows the user to specify the input file dynamically.

 Script Workflow:

1. Command-Line Argument Parsing:
   - The script starts by parsing the command-line argument to get the path to the input JSON file containing the list of packages.

2. Loading Package List:
   - It loads the list of packages from the specified JSON file.

3. Processing Each Package:
   - For each package in the list:
     - Fetches the list of versions.
     - Fetches detailed information for each version.
     - Logs the time taken to process each package.
     - Sleeps for 1 second after processing each package to respect rate limits.
     - If an error occurs during any of these steps, logs the error and adds the package to the list of failed packages.
     - Updates the JSON files (`all_package_info.json` and `failed_packages.json`) every minute.

4. Final JSON File Update:
   - After processing all packages, it performs a final update to the JSON files to ensure all collected data is saved.
