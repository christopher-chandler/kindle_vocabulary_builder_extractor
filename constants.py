# Standard
import os

from datetime import datetime
from enum import Enum

# Pip
import genanki
import yaml

# Custom
# None

# Get the current time
time_stamp = datetime.now().strftime("%m_%d_%Y_%I_%M_%S_%p")

STANDARD_CONFIG = "config.yaml"
# SECONDARY_CONFIG = ""


def load_in_yaml(file: str = STANDARD_CONFIG) -> dict:
    """
    Load YAML content from the specified file.

    Parameters:
    - file (str): Path to the YAML file.

    Returns:
    - dict: Parsed YAML content.
    """
    try:
        with open(file, mode="r") as yaml_file:
            config_contents = yaml.safe_load(yaml_file)
        return config_contents
    except FileNotFoundError:
        print(f"Error: File not found - {file}")
        return {}
    except yaml.YAMLError as e:
        print(f"Error loading YAML from {file}: {e}")
        return {}


class Configs(Enum):
    """
    These are hard-coded constants that do not require any special formatting.
    They are drawn from the config.yaml that should be located in the main directory
    of this project.
    """

    # config file loaded
    yml_config = load_in_yaml(STANDARD_CONFIG)

    # dir
    WORKING_DIRECTORY = yml_config.get("WORKING_DIRECTORY")
    LOGGING_RESULTS = yml_config.get("LOGGING_RESULTS")
    CSV_VOCAB_RESULTS = yml_config.get("CSV_VOCAB_RESULTS")

    # Anki
    ANKI_APP = yml_config.get("ANKI_APP")
    ANKI_APKG = yml_config.get("ANKI_APKG")

    # Kindle
    KINDLE_DATABASE = yml_config.get("KINDLE_DATABASE")
    DUMPED_DATA = yml_config.get("DUMPED_DATA")

    # Kindle device pickles
    KINDLE_PAPER_WHITE_VOCAB_FILE = yml_config.get("KINDLE_PAPER_WHITE_VOCAB_FILE")
    KINDLE_OASIS_VOCAB_FILE = yml_config.get("KINDLE_OASIS_VOCAB_FILE")
    KINDLE_DATABASE_FILE = yml_config.get("KINDLE_DATABASE_FILE")

    # Kindle device id
    SC_PAPER_WHITE = yml_config.get("SC_PAPER_WHITE")
    SC_KINDLE_OASIS = yml_config.get("SC_KINDLE_OASIS")


# Set the path to the main directory
os.chdir(Configs.WORKING_DIRECTORY.value)

LOG_FILE_NAME = f"logging_results/kindle_{time_stamp}.log"

# Kindle will be unmounted after all data has been extracted
EJECT_KINDLE = ["diskutil", "unmount", "/Volumes/Kindle"]

# SQL Data
SQL_BOOK_INFO_TEMPLATE = {
    "id": list(),
    "asin": list(),
    "guid": list(),
    "lang": list(),
    "title": list(),
    "authors": list(),
}

SQL_LOOKUP_TEMPLATE = {
    "id": list(),
    "word_key": list(),
    "book_key": list(),
    "dict_key": list(),
    "pos": list(),
    "usage": list(),
    "timestamp": list(),
}

# Anki Template
HEADER_SELECTION = (
    "id",
    "word_key",
    "book_key",
    "dict_key",
    "pos",
    "usage",
    "timestamp",
    "lang",
    "Translation",
    "Definitions",
    "Frequency",
    "Word Type",
    "Grammar Point",
    "Screenshot",
    "Sentence Audio",
    "Word Audio",
    "Images",
    "Example Sentences",
    "Is Vocabulary Card",
    "Is Audio Card",
    "Notes",
    "Explanation",
)

ANKI_HEADER = [{"name": head} for head in HEADER_SELECTION]
FRONT_TEMPLATE = open("vocab/flash_card_templates/front.html", mode="r").read()
BACK_TEMPLATE = open("vocab/flash_card_templates/back.html", mode="r").read()
STYLE_TEMPLATE = open(r"vocab/flash_card_templates/style.css", mode="r").read()

# Anki deck model
ANKI_MODEL = genanki.Model(
    1607392319,
    "Import Anki Deck",
    fields=ANKI_HEADER,
    templates=[
        {
            "name": "Card 1",
            "qfmt": f"{FRONT_TEMPLATE}",
            "afmt": f"{BACK_TEMPLATE}",
            "tags": "hello",
        },
    ],
    css=STYLE_TEMPLATE,
)
ANKI_DECK = genanki.Deck(deck_id=2059400110, name="Kindle")
