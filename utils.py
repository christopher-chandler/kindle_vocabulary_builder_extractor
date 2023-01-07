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

anki_model = genanki.Model(
  1607392319,
  'Simple Model',
  fields=[
    {'name': 'id'},
    {'name': 'word_key'},
{'name': 'book_key'},
    {'name': 'dict_key'},
{'name': 'pos'},
    {'name': 'usage'},
{'name': 'timestamp'},
    {'name': 'lang'},
{'name': 'lang'},
  ],
  templates=[
    {
      'name': 'Card 1',
      'qfmt': '{{Question}}',
      'afmt': '{{FrontSide}}<hr id="answer">{{Answer}}',
    },
  ])

anki_deck = genanki.Deck(
            deck_id=2059400110,
            name="Kindle Oasis")