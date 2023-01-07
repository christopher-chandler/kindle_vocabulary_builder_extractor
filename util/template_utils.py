import genanki

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

front = open("model_templates/front.html",mode="r").read()
back = open("model_templates/back.html",mode="r").read()
anki_header = 'id', 'word_key', 'book_key', 'dict_key', 'pos', 'usage', 'timestamp', 'lang', 'Translation', 'Definitions', 'Frequency', 'Word Type', 'Grammar Point', 'Screenshot', 'Sentence Audio', 'Word Audio', 'Images', 'Example Sentences', 'Is Vocabulary Card', 'Is Audio Card', 'Notes', 'Explanation'

f = [{"name": head} for head in anki_header]

anki_model = genanki.Model(
    1607392319,
    "Simple Model",
    fields=f,
    templates=[
        {
            "name": "Card 1",
            "qfmt": f"{front}",
            "afmt": f"{back}",
            "tags":"hello"
        },
    ],
)

anki_deck = genanki.Deck(deck_id=2059400110, name="Kindle Oasis")

