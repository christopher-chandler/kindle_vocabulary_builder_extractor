# Standard
import os
import json

# Pip
import yaml

# Custom
# None

"""
In order for KindleLex to work, you have to properly set up the configuration file. 
Most of the configs should work out of the box, 
the only setting that needs to be changed is the home directory of the working app 
"""


def get_config_data(file: str = None) -> dict:
    """
    Reads configuration data from a YAML file and returns it as
    a Python data structure.

    Args:
    file (str): The file path to the YAML configuration file.
        If not specified, the default configuration file 'config.yaml'
        in the script's directory will be used.

    Returns:
        config_data (dict): A Python dictionary containing the configuration data.
    """
    if file is None:
        # The directory where the script is located
        script_directory = os.path.dirname(os.path.abspath(__file__))

        # The path to the YAML configuration file relative to the script's directory
        file = os.path.join(
            script_directory,
            "settings_files/settings.yaml",
        )

    # Load the YAML configuration file
    with open(file, mode="r", encoding="utf-8") as config_file:
        config_data: dict = yaml.safe_load(config_file)

    return {"config_data": config_data, "file": file}


def set_working_directory():
    config_data, file = list(get_config_data().values())
    config_data["WORKING_DIRECTORY"] = os.getcwd()

    with open(file, mode="w+", encoding="utf-8") as config_file:
        yaml.dump(config_data, config_file)


if __name__ == "__main__":
    set_working_directory()
