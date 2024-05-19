# Standard
import datetime
import os

# Pip
import genanki

# Custom
from kindle_lex.settings.constants.constant_paths import GeneralPaths as Gp

print(os.getcwd())
"""
Hier sind Konstanten, die von anderen Funktionen verwendet werden. 
"""

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
FRONT_TEMPLATE = open(
    "resources/flash_card_templates/front.html",
    mode="r",
).read()
BACK_TEMPLATE = open(
    "resources/flash_card_templates/back.html",
    mode="r",
).read()
STYLE_TEMPLATE = open(
    r"resources/flash_card_templates/style.css",
    mode="r",
).read()

# Anki deck model
ANKI_MODEL = genanki.Model(
    1607392319,
    "Kindle Import",
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

if __name__ == "__main__":
    pass
