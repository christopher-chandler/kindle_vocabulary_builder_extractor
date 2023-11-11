# Standard
import csv
import logging
import pickle
import os
import sqlite3

from datetime import datetime

# Pip
import genanki
import typer

# Custom
from app_util.constants import (
    SQL_BOOK_INFO_TEMPLATE,
    SQL_LOOKUP_TEMPLATE,
    KINDLE_DATABASE,
    RESULTS_FOLDER,
    ANKI_MODEL,
    HEADER_SELECTION,
    WORKING_DIRECTORY,
)

os.chdir(WORKING_DIRECTORY)


def main_extractor(**kwargs) -> bool:
    # SQL Cursor

    device_name = kwargs.get("device_name")
    dump_ids = kwargs.get("dump_ids")
    only_allow_unique_ids = kwargs.get("only_allow_unique_ids")
    vocab_key_reference = kwargs.get("vocab_key_reference")
    vocab_database = sqlite3.connect(KINDLE_DATABASE)
    cursor = vocab_database.cursor()

    book_info_cursor = cursor.execute("SELECT * from BOOK_INFO")
    book_info_output = book_info_cursor.fetchall()

    lookup_cursor = cursor.execute("SELECT * from LOOKUPS")
    lookup_cursor_output = lookup_cursor.fetchall()

    id_db = list()
    SQL_BOOK_INFO = dict()

    for row in book_info_output:
        temp_dict = dict()
        for entry, table_name in zip(row, SQL_BOOK_INFO_TEMPLATE.keys()):
            temp_dict[table_name] = entry

            word_id = temp_dict.get("id")
            SQL_BOOK_INFO[word_id] = temp_dict

    SQL_LOOKUPS = dict()
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
        book, lang = (
            SQL_BOOK_INFO[temp_dict["book_key"]]["title"].replace(" ", "_"),
            temp_dict["lang"],
        )

        temp_dict["tag"] = [book.replace(" ", "_"), lang]
        temp_dict["book_key"] = SQL_BOOK_INFO[temp_dict["book_key"]]["title"]
        word_id = temp_dict["id"]
        SQL_LOOKUPS[word_id] = temp_dict
        id_db.append(word_id)

    if dump_ids:
        with open(f"vocab_data/{device_name}.pkl", "wb") as pickle_file:
            pickle.dump(id_db, pickle_file)

    with open(
        f"{RESULTS_FOLDER}/{device_name}.csv", mode="w+", encoding="utf-8"
    ) as save_file:

        if device_name == "kindle_oasis":
            deck_id = 2059400110
        else:
            deck_id = 2059400111

        unique_notes = list()
        ANKI_DECK = genanki.Deck(deck_id=deck_id, name=device_name)

        for sql_entry in SQL_LOOKUPS:
            header = list(SQL_LOOKUPS.get(sql_entry).keys())
            break
        csv_dictwriter = csv.DictWriter(save_file, header)
        csv_dictwriter.writeheader()

        for sql_entry in SQL_LOOKUPS:
            entry = SQL_LOOKUPS.get(sql_entry)
            csv_dictwriter.writerow(entry)

            for head in HEADER_SELECTION:
                if head not in entry:
                    entry[head] = " "
            tags = entry.get("tag")
            tags.append(device_name)

            entry.pop("tag")

            anki_note = genanki.Note(
                model=ANKI_MODEL, fields=list(entry.values()), tags=tags
            )

            if only_allow_unique_ids:

                note_id = entry.get("id")
                if note_id not in vocab_key_reference:
                    unique_notes.append(note_id)
                    ANKI_DECK.add_note(anki_note)
            else:
                ANKI_DECK.add_note(anki_note)

        if len(unique_notes) == 0:
            no_new_notes = "No new notes could be found."
            logging.info(no_new_notes)
            typer.secho(no_new_notes, fg=typer.colors.BRIGHT_RED)
            return False

        else:
            unique_notes = f"{len(unique_notes)} note(s) were found."
            typer.secho(unique_notes)
            logging.info(unique_notes)
            deck = genanki.Package(ANKI_DECK)
            deck.write_to_file(f"{RESULTS_FOLDER}/{device_name}.apkg")

            return True
