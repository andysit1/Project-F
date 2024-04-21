import os
import sys
import json

# Setup the environment by appending the current directory to the system path for asset access.
src_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(src_dir)

def save_settings(settings, filename, file_path=os.path.join(src_dir)):
    """
    Saves settings to a JSON file.

    Args:
        settings: The settings to save.
        filename (str): The name of the file to save to.
        file_path (str, optional): The path to save the file to. Defaults to 'src/saves/'.
    """

    with open(file_path + filename, 'w') as file:
        json.dump(settings, file)

def load_settings(filename, file_path=os.path.join(src_dir)):
    """
    Loads settings from a JSON file.

    Args:
        filename (str): The name of the file to load.
        file_path (str, optional): The path to load the file from. Defaults to 'src/saves/'.

    Returns:
        dict: The loaded settings.
    """
    try:
        with open(file_path + filename, 'r') as file:
            settings = json.load(file)
            return settings
    except FileNotFoundError:
        print("Settings file not found.")
        return None
