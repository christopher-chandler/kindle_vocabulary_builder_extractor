# Standard
from datetime import datetime

# Pip
import typer.colors

# Custom
from kindle_lex.settings.constants.constant_paths import GeneralPaths as Gp
from kindle_lex.settings.logger.basic_logger import (
    catch_and_log_error,
    catch_and_log_info,
)

from kindle_lex.amazon.database_interface.database_getter import DatabaseGetter
from kindle_lex.settings.constants.constant_vars import (
    SQL_LOOKUP_TEMPLATE,
    SQL_BOOK_INFO_TEMPLATE,
)


class DatabaseProcessor(DatabaseGetter):
    """
    tests

    """

    def __init__(
        self,
        device_name: str,
        dump_ids: bool,
        only_allow_unique_ids: bool,
        vocab_key_reference: str,
        initial_id_dump: bool,
    ):
        super().__init__(
            device_name, dump_ids, only_allow_unique_ids, vocab_key_reference
        )
        self.initial_id_dump = initial_id_dump

    def process_book_info(self):
        """

        :return:
        """
        SQL_BOOK_INFO = dict()

        book_info_output = self.get_book_info()

        # Process data from BOOK_INFO table
        for row in book_info_output:
            temp_dict = dict()
            for entry, table_name in zip(row, SQL_BOOK_INFO_TEMPLATE.keys()):
                temp_dict[table_name] = entry

                word_id = temp_dict.get("id")
                SQL_BOOK_INFO[word_id] = temp_dict

        return SQL_BOOK_INFO

    def process_lookups(self) -> list:

        id_db = list()

        lookup_cursor_output = self.get_lookups()
        SQL_BOOK_INFO = self.process_book_info()
        SQL_LOOKUPS = self.process_book_info()

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

        # Removing unused keys
        keys_to_remove = ["asin", "guid", "title", "authors"]

        # First remove specific keys from each entry
        for entry in list(
            SQL_LOOKUPS
        ):  # Convert to list to avoid modifying during iteration
            for key in keys_to_remove:
                SQL_LOOKUPS[entry].pop(key, None)

        # Then remove entries where the length of the dictionary is not 9
        for entry in list(SQL_LOOKUPS):  # Again, use a list for safe removal
            if len(SQL_LOOKUPS[entry]) != 9:
                SQL_LOOKUPS.pop(entry)

        results = {"id_db": id_db, "SQL_LOOKUPS": SQL_LOOKUPS}

        return results


if __name__ == "__main__":

    db_getter = DatabaseProcessor(
        device_name="Kindle",
        dump_ids=True,
        only_allow_unique_ids=True,
        vocab_key_reference="",
        initial_id_dump=True,
    )
    print(db_getter.process_lookups())
