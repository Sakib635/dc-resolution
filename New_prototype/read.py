import json
import os


def read_requirements(directory):
    """
    Reads the content of the `requirements.txt` file from a specified directory.

    Parameters:
        directory (str): The path to the directory containing the `requirements.txt` file.

    Returns:
        str: The content of the `requirements.txt` file as a single string.
    """
    with open(os.path.join(directory, "r.txt"), "r") as file:
        return file.read()


# Function to read the JSON file from a directory
def read_json_file(directory, filename="KBase.json"):
    """
    Reads the content of a JSON file from a specified directory.

    Parameters:
        directory (str): The path to the directory containing the JSON file.
        filename (str): The name of the JSON file to read. Default is 'updated_formated_8k.json'.

    Returns:
        dict: The content of the JSON file as a dictionary.
    """
    with open(os.path.join(directory, filename), "r") as file:
        return json.load(file)
