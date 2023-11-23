# Standard
import pickle
import random
import os

from datetime import datetime
from enum import Enum

# Pip
import genanki
import yaml

# Custom
# None


def load_in_yaml(file: str = "config.yaml"):

    with open(file, mode="r") as yaml_file:
        config_contents = yaml.safe_load(yaml_file)

    return config_contents


class Configs(Enum):
    """
    These are hard-coded constants that do not required any special formatting.
    They are drawn from the config.yaml that should me located in the main directory
    of this project .
    """

    yml_config = load_in_yaml()

    # dir
    WORKING_DIRECTORY = yml_config.get("WORKING_DIRECTORY")
    LOGGING_RESULTS = yml_config.get("LOGGING_RESULTS")
    CSV_VOCAB_RESULTS = yml_config.get("CSV_VOCAB_RESULTS")


# Set the path to the main directory
os.chdir(Configs.WORKING_DIRECTORY.value)

# Get the current time
time_stamp_string = datetime.now().strftime("%m_%d_%Y_%I_%M_%S_%p")

LOG_FILE_NAME = f"log_results/kindle_{time_stamp_string}.log"
LOG_FOLDER = (
    r"/Users/christopherchandler/repo/Python"
    r"/kindle_vocabulary_builder_extractor/log_dir"
)
RESULTS_FOLDER = (
    "/Users/christopherchandler/"
    "repo/Python/kindle_vocabulary_builder_extractor/results"
)
KINDLE_DATABASE = "/Volumes/Kindle/System/vocabulary/vocab.db"
EJECT_KINDLE = ["diskutil", "unmount", "/Volumes/Kindle"]

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

#
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

KINDLE_PAPER_WHITE_VOCAB_FILE = r"vocab/dumped_kindle_data/kindle_paper_white.pkl"
KINDLE_OASIS_VOCAB_FILE = r"vocab/dumped_kindle_data/kindle_oasis.pkl"
SC_PAPER_WHITE = "G000T60783540207"
SC_KINDLE_OASIS = "G000WM0602110684"
