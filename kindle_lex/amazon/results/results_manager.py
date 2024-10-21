# Standard
import csv
import logging
import subprocess
import random

# Pip
import genanki
import typer

# Custom

# Constants
from kindle_lex.settings.constants.constant_paths import GeneralPaths as Gp
from kindle_lex.settings.logger.basic_logger import catch_and_log_info
from kindle_lex.settings.constants.constant_vars import (
    ANKI_MODEL,
    ANKI_HEADER_SELECTION,
)

from kindle_lex.amazon.database_interface.database_processor import DatabaseProcessor
from kindle_lex.amazon.database_interface.database_pickler import DatabasePickler

unique_notes = list()


class ResultsManager(DatabaseProcessor):
    def __init__(
        self,
        anki_deck_name: str,
        device_name: str,
        dump_ids: bool,
        only_allow_unique_ids: bool,
        vocab_key_reference: list,
        initial_id_dump: bool,
    ):

        super().__init__(
            device_name,
            dump_ids,
            only_allow_unique_ids,
            vocab_key_reference,
            initial_id_dump,
        )

        self.SQL_LOOKUPS = self.process_lookups().get("SQL_LOOKUPS")
        self.anki_deck_name = anki_deck_name

    def import_deck(self) -> None:
        """
        Import an Anki deck into the Anki application.

        Parameters:
        - name (str): The name of the Anki deck to import.

        Returns:
        - None

        Notes:
        - This function uses the Anki application specified in the Configs module.
        - The imported deck file should be located in the directory specified by
        Configs.ANKI_VOCAB_RESULTS.
        - If the Anki application is not found or the specified deck file does not exist,
        the function will not raise an exception,
        but the import may not be successful.

        """
        anki_deck_name = self.anki_deck_name

        filename = f"{Gp.ANKI_APKG.value}/{anki_deck_name}.apkg"
        anki_app = Gp.ANKI_APP.value
        subprocess.run(["open", "-a", anki_app, filename])

        catch_and_log_info(
            custom_message="The deck is being imported...",
            echo_msg=True,
            echo_color=typer.colors.GREEN,
        )

    def __save_files(self):
        device_name = self.device_name

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
        SQL_LOOKUPS = self.process_lookups().get("SQL_LOOKUPS")

        dict_writer_field_names = (
            "id,word_key,book_key,dict_key,pos,usage,timestamp," "lang,tag"
        ).split(",")

        all_entries_csv_dict_writer = csv.DictWriter(
            all_entries, dict_writer_field_names
        )
        current_entries_csv_dict_writer = csv.DictWriter(
            current_entries, dict_writer_field_names
        )

        deck_id = random.randint(1, 2059400111)

        ANKI_DECK = genanki.Deck(deck_id=deck_id, name=device_name)

        save_files = {
            "all_entries": all_entries_csv_dict_writer,
            "current_entries": current_entries_csv_dict_writer,
            "ANKI_DECK": ANKI_DECK,
        }

        return save_files

    def write_data(self):

        ids = list()

        all_entries_csv_dict_writer = self.__save_files().get("all_entries")
        current_entries_csv_dict_writer = self.__save_files().get("current_entries")
        ANKI_DECK = self.__save_files().get("ANKI_DECK")

        all_entries_csv_dict_writer.writeheader()

        device_name = self.device_name
        dp = DatabasePickler(device_name=device_name, vocab_pickle=device_name)

        all_entries_csv_dict_writer.writeheader()
        current_entries_csv_dict_writer.writeheader()
        SQL_LOOKUPS = self.process_lookups().get("SQL_LOOKUPS")

        for sql_entry in SQL_LOOKUPS:
            entry = SQL_LOOKUPS.get(sql_entry)

            all_entries_csv_dict_writer.writerow(entry)
            if id not in dp.get_pickle_data():
                current_entries_csv_dict_writer.writerow(entry)

            for head in ANKI_HEADER_SELECTION:
                if head not in entry:
                    entry[head] = " "
            tags = entry.get("tag")
            if tags is not None:
                tags.append(device_name)
                entry.pop("tag")

            if id not in dp.get_pickle_data():

                anki_note = genanki.Note(
                    model=ANKI_MODEL, fields=list(entry.values()), tags=tags
                )

                ANKI_DECK.add_note(anki_note)

        # Create anki decks
        deck = genanki.Package(ANKI_DECK)
        deck.write_to_file(f"{Gp.ANKI_APKG.value}/{device_name}.apkg")

        typer.echo("Wrote to csv file")
        return len(ids)

    def write_to_anki_package(self):

        ANKI_DECK = self.__save_files().get("ANKI_DECK")
        device_name = self.device_name

        SQL_LOOKUPS = self.SQL_LOOKUPS

        for sql_entry in SQL_LOOKUPS:
            entry = SQL_LOOKUPS.get(sql_entry)

            for head in ANKI_HEADER_SELECTION:
                if head not in entry:
                    entry[head] = " "
            tags = entry.get("tag")
            if tags is not None:
                tags.append(device_name)
                entry.pop("tag")

            anki_note = genanki.Note(
                model=ANKI_MODEL, fields=list(entry.values()), tags=tags
            )

            ANKI_DECK.add_note(anki_note)

        # Create anki decks
        deck = genanki.Package(ANKI_DECK)
        deck.write_to_file(f"{Gp.ANKI_APKG.value}/{device_name}.apkg")

    def unique_note_information(self):

        unique_notes = list()

        SQL_LOOKUPS = self.process_lookups().get("SQL_LOOKUPS")
        device_name = self.device_name
        dp = DatabasePickler(device_name=device_name, vocab_pickle=device_name)

        for sql_entry in SQL_LOOKUPS:
            entry = SQL_LOOKUPS.get(sql_entry)

            id = entry.get("id")

            if id not in dp.get_pickle_data():
                unique_notes.append(id)

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

            unique_notes_info = f"{len(unique_notes)} notes  found."
            self.write_data()

            # Log info
            typer.secho(unique_notes_info)
            logging.info(unique_notes_info)

            return True


if __name__ == "__main__":

    rm = ResultsManager(
        anki_deck_name="",
        device_name="SC_KINDLE_OASIS",
        dump_ids=True,
        only_allow_unique_ids=True,
        vocab_key_reference=[],
        initial_id_dump=True,
    )
    r = rm.write_data()
    print(r)
