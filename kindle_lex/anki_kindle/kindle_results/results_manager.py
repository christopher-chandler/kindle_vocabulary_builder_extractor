# Standard
import csv
import logging
import subprocess
import random
import re

from datetime import datetime

# Pip
import genanki
import typer

# Custom

# Constants
from kindle_lex.settings.constants.constant_paths import GeneralPaths as Gp


# Logger
from kindle_lex.settings.logger.basic_logger import catch_and_log_info


from kindle_lex.anki_kindle.kindle.kindle_db_processor import KindleDBProcessor
from kindle_lex.settings.constants.constant_vars import (
    ANKI_MODEL,
    ANKI_HEADER_SELECTION,
)

unique_notes = list()


class ResultsManager(KindleDBProcessor):
    def __init__(
        self,
        anki_deck_name: str = "kindle_import",
        device_name: str="kindle",
        dump_ids: bool=True,
        only_allow_unique_ids: bool = True,
        vocab_key_reference: list = None,
        initial_id_dump: bool = False,

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

    def __save_files(self) -> dict:
        """
        This saves the results from the kindle vocab dump to the respective file type.

        Parameters:
            None

        :return:
            save_files (dict): this is a dictionary of the csv writeres (all, current) and
            the anki dict writer so that the results can be saved to the respective
            objects
        """
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

        # Create field names
        dict_writer_field_names = (
            "id,word_key,book_key,dict_key,pos,usage,timestamp,lang,tag").split(",")

        # CSV Dict writer
        all_entries_csv_dict_writer = csv.DictWriter(
            all_entries, dict_writer_field_names
        )
        current_entries_csv_dict_writer = csv.DictWriter(
            current_entries, dict_writer_field_names
        )

        # Anki package base
        anki_deck_id = random.randint(1, 2059400111)
        anki_deck = genanki.Deck(deck_id=anki_deck_id, name=device_name)

        save_files = {
            "all_entries": all_entries_csv_dict_writer,
            "current_entries": current_entries_csv_dict_writer,
            "anki_deck": anki_deck,
        }

        return save_files

    def write_to_csv(self, result_filter_keys:dict = None) -> None:
        """

        :return:
            None
        """
        # Assign dict writeres
        all_entries_csv_dict_writer = self.__save_files().get("all_entries")
        current_entries_csv_dict_writer = self.__save_files().get("current_entries")

        # Add headers to files
        all_entries_csv_dict_writer.writeheader()
        current_entries_csv_dict_writer.writeheader()

        SQL_LOOKUPS = self.process_lookups().get("SQL_LOOKUPS")

        for sql_entry in SQL_LOOKUPS:

            entry = SQL_LOOKUPS.get(sql_entry)
            

            # converts to comparable date format
            timestamp = datetime.strptime(entry.get(
             "timestamp", ""), '%B %d, %Y %I:%M:%S %p')

            word_key = entry.get("word_key", None)
            book_key = entry.get("book_key", None)

            usage = entry.get("usage", None)
            lang = entry.get("lang", None)


            if result_filter_keys is not None:

                usage_compare = result_filter_keys.get("usage", None)

                time = entry.get("timestamp","")

                if time:
                    timestamp = datetime.strptime(time, '%B %d, %Y %I:%M:%S %p')
                    other_time = result_filter_keys.get("timestamp")

                    if timestamp > other_time:
                        print(timestamp)
            else:

                all_entries_csv_dict_writer.writerow(entry)


    def write_to_anki_package(self):

        anki_deck = self.__save_files().get("anki_deck")
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

            anki_deck.add_note(anki_note)

        # Create anki decks
        deck = genanki.Package(anki_deck)
        deck.write_to_file(f"{Gp.ANKI_APKG.value}/{device_name}.apkg")

    def unique_note_information(self):

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

            return True


if __name__ == "__main__":

    rm = ResultsManager(
        anki_deck_name="",
        device_name="Kindle",
        dump_ids=True,
        only_allow_unique_ids=True,
        vocab_key_reference=[],
        initial_id_dump=True,

    )
    r = rm.write_to_csv(

        result_filter_keys={"usage": re.compile("店内"),
                            "timestamp": datetime(2023, 10, 1)}




    )
    print(r)
