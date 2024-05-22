import requests
import time
import json
from packaging.version import parse


def fetch_versions(package_name):
    """Fetch the list of versions for a given package."""
    url = f"https://pypi.org/pypi/{package_name}/json"
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Failed to fetch versions for {package_name}: {response.status_code}")
        return []
    
    data = response.json()
    versions = list(data["releases"].keys())
    #versions.sort(key=parse, reverse=True)
    return versions

def fetch_package_info(package_name, version=None):
    """Fetch the required information for a specific version of a package."""
    if version:
        url = f"https://pypi.org/pypi/{package_name}/{version}/json"
    else:
        url = f"https://pypi.org/pypi/{package_name}/json"
        
    response = requests.get(url, headers={'Accept': 'application/json'})
    if response.status_code == 200:
        root = response.json()
        if "info" in root:
            info = root['info']
            return {
                "package_name": info.get('name'),
                "version": info.get('version'),
                "dependency_packages": info.get("requires_dist"),
                "python_version": info.get("requires_python")
            }
    return None

def update_json_file(data, filename):
    """Update the JSON file with the given data."""
    with open(filename, 'w') as f:
        json.dump(data, f, indent=2)
        print(f"Updated {filename} with collected data.")

def main(projects):
    package_info_list = []
    failed_packages = []
    package_info_filename = 'all_package_info.json'
    failed_packages_filename = 'failed_packages.json'

    start_time = time.time()
    last_update_time = start_time

    for package_name in projects:
        package_start_time = time.time()

        try:
            versions = fetch_versions(package_name)
            if not versions:
                # If no versions, fetch info from package JSON endpoint
                info = fetch_package_info(package_name)
                if info:
                    package_info_list.append(info)
                else:
                    failed_packages.append(package_name)
            else:
                for version in versions:
                    info = fetch_package_info(package_name, version)
                    if info:
                        package_info_list.append(info)
                    else:
                        failed_packages.append(package_name)
        except Exception as e:
            print(f"Error occurred for {package_name}: {e}")
            failed_packages.append(package_name)

        # Sleep for 1 second after every package processed
        time.sleep(1)
        
        # Calculate and print time taken for the package
        package_end_time = time.time()
        package_time_taken = package_end_time - package_start_time
        print(f"Time taken for {package_name}: {package_time_taken:.2f} seconds")

        # Update JSON file every minute
        if time.time() - last_update_time >= 60:
            update_json_file(package_info_list, package_info_filename)
            update_json_file(failed_packages, failed_packages_filename)
            last_update_time = time.time()

    # Final update to JSON file after all packages are processed
    update_json_file(package_info_list, package_info_filename)
    update_json_file(failed_packages, failed_packages_filename)

if __name__ == "__main__":
    json_file_path = "directory of JSON file" #"C:/Users/sakib51/Downloads/Pypi info collection dataset/packageList.json"

    with open(json_file_path, 'r') as j:
        contents = json.loads(j.read())
    print(type(contents),len(contents),contents[0:5])
    main(contents)


