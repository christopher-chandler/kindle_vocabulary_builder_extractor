# Standard
import datetime

# Pip
import genanki

# Custom
from kindle_lex.device_system_manager.file_manager import open_template

"""
Constants used by other functions 
"""

LOG_DIR = "log_res"

current_datetime = datetime.datetime.now()
TIMESTAMP = current_datetime.strftime("%Y_%m_%d_%H_%M_%S")
SIMPLE_TIMESTAMP = current_datetime.strftime("%Y_%m_%d")

LOG_FILE_NAME = f"logging_results/kindle_{TIMESTAMP}.log"

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
ANKI_HEADER_SELECTION = (
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
    "Explanation"
)

ANKI_HEADER = [{"name": head} for head in ANKI_HEADER_SELECTION]
ANKI_DECK = genanki.Deck(deck_id=2059400110, name="Kindle")

# Anki deck model
MODEL_NAME = "KN - Kindle Import"
MODEL_ID = 1607392319
CARD_NAME = "Kindle Card"

ANKI_MODEL = genanki.Model(
    MODEL_ID,
    MODEL_NAME,
    fields=ANKI_HEADER,
    templates=[
        {
            "name": CARD_NAME,
            "qfmt": open_template("resources/flash_card_templates/front.html"),
            "afmt": open_template("resources/flash_card_templates/back.html"),
            "tags": "hello",
        },
    ],
    css=open_template("resources/flash_card_templates/style.css"),
)

WAITING_TIME_IN_SECONDS = 5

if __name__ == "__main__":
    pass
