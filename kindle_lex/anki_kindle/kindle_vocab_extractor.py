# Standard
import csv
import logging
import pickle
import os
import random
import sqlite3

from datetime import datetime
from copy import deepcopy

# Pip
import genanki
import typer

# Custom
from kindle_lex.settings.constants.constant_vars import (
    SQL_LOOKUP_TEMPLATE,
    SQL_BOOK_INFO_TEMPLATE,
    ANKI_MODEL,
    ANKI_HEADER_SELECTION,
)

from kindle_lex.settings.constants.constant_paths import GeneralPaths as Gp
from kindle_lex.settings.logger.basic_logger import catch_and_log_info

# Change current working directory to the specified directory
os.chdir(Gp.WORKING_DIRECTORY.value)




def main_extractor(**kwargs) -> bool:
    """
    Extracts Kindle vocabulary data, processes it, and generates Anki notes.

    Parameters:
    - kwargs (dict): Keyword arguments controlling the extraction and processing.

    Keyword Arguments:
    - device_name (str): Name of the Kindle device.
    - dump_ids (bool): Whether to dump vocabulary IDs to a pickle file.
    - only_allow_unique_ids (bool): Whether to allow only unique vocabulary IDs.
    - vocab_key_reference (list): List of reference vocabulary keys.

    Returns:
    - bool: True if extraction and processing were successful, False otherwise.
    """
    device_name = kwargs.get("device_name")
    dump_ids = kwargs.get("dump_ids")
    initial_id_dump = kwargs.get("initial_id_dump")
    only_allow_unique_ids = kwargs.get("only_allow_unique_ids")
    vocab_key_reference = kwargs.get("vocab_key_reference")

    # Connect to the Kindle vocabulary database
    vocab_database = sqlite3.connect(Gp.KINDLE_DATABASE.value)
    cursor = vocab_database.cursor()

    # Retrieve data from BOOK_INFO table
    book_info_cursor = cursor.execute("SELECT * from BOOK_INFO")
    book_info_output = book_info_cursor.fetchall()

    # Retrieve data from LOOKUPS table
    lookup_cursor = cursor.execute("SELECT * from LOOKUPS")
    lookup_cursor_output = lookup_cursor.fetchall()

    id_db = list()
    SQL_BOOK_INFO = dict()

    # Process data from BOOK_INFO table
    for row in book_info_output:
        temp_dict = dict()
        for entry, table_name in zip(row, SQL_BOOK_INFO_TEMPLATE.keys()):
            temp_dict[table_name] = entry

            word_id = temp_dict.get("id")
            SQL_BOOK_INFO[word_id] = temp_dict

    SQL_LOOKUPS = dict()
    # Process data from LOOKUPS table
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

    # Dump IDs to a pickle file if specified
    if dump_ids:
        with open(f"{Gp.DUMPED_DATA.value}/{device_name}.pkl", "wb") as pickle_file:
            pickle.dump(id_db, pickle_file)

    if initial_id_dump:
        with open(f"{Gp.DUMPED_DATA.value}/{device_name}.pkl", "wb") as pickle_file:
            pickle.dump(id_db, pickle_file)
        raise SystemExit("Id files initially dumped. Restart the program.")

    # Gather entires

    all_entries = open(
        f"{Gp.CSV_VOCAB_RESULTS.value}/{device_name}.csv",
        mode="w+",
        encoding="utf-8",
    )
    current_entries = open(
        f"{Gp.CURRENT_RESULTS.value}current_results_{device_name}.csv",
        mode="w+",
        encoding="utf-8",
    )

    # Write data to a CSV file

    deck_id = random.randint(1, 2059400111)
    unique_notes = list()
    ANKI_DECK = genanki.Deck(deck_id=deck_id, name=device_name)

    # Get the keys of the first entry in SQL_LOOKUPS as the header
    dict_writer_field_names = list(next(iter(SQL_LOOKUPS.values())).keys())

    all_entries_csv_dict_writer = csv.DictWriter(all_entries, dict_writer_field_names)
    current_entries_csv_dict_writer = csv.DictWriter(
        current_entries, dict_writer_field_names
    )

    all_entries_csv_dict_writer.writeheader()
    current_entries_csv_dict_writer.writeheader()

    for sql_entry in SQL_LOOKUPS:
        entry = SQL_LOOKUPS.get(sql_entry)
        entry_copy = deepcopy(entry)

        all_entries_csv_dict_writer.writerow(entry)

        for head in ANKI_HEADER_SELECTION:
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
                current_entries_csv_dict_writer.writerow(entry_copy)
                ANKI_DECK.add_note(anki_note)
        else:
            ANKI_DECK.add_note(anki_note)

    # Log and print information about the extraction result
    if len(unique_notes) == 0:
        no_new_notes = "No new notes could be found."

        catch_and_log_info(
            custom_message=no_new_notes,
            echo_msg=True,
            log_info_message=True,
            echo_color=typer.colors.BRIGHT_RED,
        )

        return False

    else:

        if len(unique_notes) == 1:
            unique_notes_info = f"{len(unique_notes)} note was found."
        else:
            unique_notes_info = f"{len(unique_notes)} notes were found."

        # Log info
        typer.secho(unique_notes_info)
        logging.info(unique_notes_info)

        # Add to anki package
        deck = genanki.Package(ANKI_DECK)
        deck.write_to_file(f"{Gp.ANKI_APKG.value}/{device_name}.apkg")

        return True


if __name__ == "__main__":
    pass
