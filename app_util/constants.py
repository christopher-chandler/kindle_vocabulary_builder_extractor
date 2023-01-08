# Standard
import pickle
import random
import os

from datetime import datetime

# Pip
import genanki

# Custom
# None

# Get the current time
time_stamp_string = datetime.now().strftime("%m_%d_%Y_%I_%M_%S_%p")
WORKING_DIRECTORY = "/Users/christopherchandler/Github" \
                    "/Python/kindle_vocabulary_builder_extractor"

os.chdir(WORKING_DIRECTORY)

LOG_FILE_NAME = f"log_dir/kindle_{time_stamp_string}.log"
LOG_FOLDER = r"/Users/christopherchandler/Github/Python" \
             r"/kindle_vocabulary_builder_extractor/log_dir"
RESULTS_FOLDER = "/Users/christopherchandler/" \
                 "Github/Python/kindle_vocabulary_builder_extractor/results"
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
FRONT_TEMPLATE = open("model_templates/front.html", mode="r").read()
BACK_TEMPLATE = open("model_templates/back.html", mode="r").read()
STYLE_TEMPLATE = open(r"model_templates/style.css", mode="r").read()

ANKI_MODEL = genanki.Model(
    1607392319,
    "Kindle Model",
    fields=ANKI_HEADER,
    templates=[
        {"name": "Card 1", "qfmt":
            f"{FRONT_TEMPLATE}", "afmt": f"{BACK_TEMPLATE}", "tags": "hello"},
    ],
    css=STYLE_TEMPLATE
)

ANKI_DECK = genanki.Deck(deck_id=2059400110, name="Kindle")
KINDLE_PAPER_WHITE_VOCAB_FILE = r"vocab_data/kindle_paper_white.pkl"
KINDLE_OASIS_VOCAB_FILE = r"vocab_data/kindle_oasis.pkl"

# initalize pickle

c = 0








