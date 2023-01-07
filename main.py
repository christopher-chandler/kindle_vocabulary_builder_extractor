# Standard
import csv
import sqlite3

from datetime import datetime

#pip
import genanki

# Custom
from utils import SQL_BOOK_INFO_TEMPLATE, SQL_LOOKUP_TEMPLATE
from utils import anki_model,anki_deck



# SQL Cursor
vocab_database = sqlite3.connect("vocab_data/vocab.db")
cursor = vocab_database.cursor()

book_info_cursor = cursor.execute("SELECT * from BOOK_INFO")
book_info_output = book_info_cursor.fetchall()

lookup_cursor = cursor.execute("SELECT * from LOOKUPS")
lookup_cursor_output = lookup_cursor.fetchall()

book_info_results = dict()
lookup_results = dict()

save_file = open("results/results.csv",mode="w",encoding="utf-8")
csv_writer = csv.writer(save_file)

SQL_BOOK_INFO=dict()

for row in book_info_output:
    temp_dict = dict()
    for entry, table_name in zip(row, SQL_BOOK_INFO_TEMPLATE.keys()):
        temp_dict[table_name] = entry

        id = temp_dict.get("id")
        SQL_BOOK_INFO[id]=temp_dict

SQL_LOOKUPS=dict()
for row in lookup_cursor_output:
    temp_dict = dict()
    for entry, table_name in zip(row, SQL_LOOKUP_TEMPLATE.keys()):
        temp_dict[table_name] = entry

    dt_object = datetime.fromtimestamp(temp_dict["timestamp"] / 1000)
    time_stamp = dt_object.strftime("%B %d, %Y %I:%M:%S %p")
    temp_dict["timestamp"] = time_stamp
    lang, word = temp_dict["word_key"].split(":")
    temp_dict["lang"] = lang
    temp_dict["word_key"] = word
    book, lang = temp_dict["book_key"].replace(" ", "_"), temp_dict["lang"]
    tag = " ".join((book, lang))
    temp_dict["tag"] = tag
    temp_dict["book_key"]=SQL_BOOK_INFO[temp_dict["book_key"]]["title"]
    id=temp_dict["id"]
    SQL_LOOKUPS[id] = temp_dict


with open("results/oasis.csv",mode="w",encoding="utf-8") as save_file:

    for i in SQL_LOOKUPS:
        header = list(SQL_LOOKUPS.get(i).keys())
        break
    csv_dictwriter = csv.DictWriter(save_file, header)


    for i in SQL_LOOKUPS:
        entry = SQL_LOOKUPS.get(i)

        csv_dictwriter.writerow(entry)
        my_note = genanki.Note(
            model=anki_model,
            fields=list(entry.values()))
        anki_deck.add_note(my_note)

deck  = genanki.Package(anki_deck)
save_deck = deck.write_to_file('oasis.apkg')

