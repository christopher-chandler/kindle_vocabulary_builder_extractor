# Standard
import pickle

from datetime import datetime

# Pip
# None

# Custom
from kindle_lex.settings.constants.constant_paths import GeneralPaths as Gp
from kindle_lex.settings.logger.basic_logger import catch_and_log_info

from kindle_lex.anki_kindle.kindle.kindle_db_getter import KindleDBGetter
from kindle_lex.settings.constants.constant_vars import (
    SQL_LOOKUP_TEMPLATE,
    SQL_BOOK_INFO_TEMPLATE,

)


class KindleDBProcessor(KindleDBGetter):
    """
    tests

    """

    def __init__(
        self,
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
            vocab_key_reference
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
        keys_to_remove = ['asin', 'guid', 'title', 'authors']
        for entry in SQL_LOOKUPS:
            for key in keys_to_remove:
                SQL_LOOKUPS.get(entry).pop(key, None)

        results = {"id_db": id_db, "SQL_LOOKUPS": SQL_LOOKUPS}

        return results

    def dump_ids_to_pickle(self):
        initial_id_dump = self.initial_id_dump
        dump_ids = self.dump_ids
        device_name = self.device_name

        id_db = self.process_lookups().get("id_db")

        # Dump IDs to a pickle file if specified
        if dump_ids:
            with open(f"{Gp.DUMPED_DATA.value}/{device_name}.pkl", "wb") as pickle_file:
                pickle.dump(id_db, pickle_file)

        if initial_id_dump:
            with open(f"{Gp.DUMPED_DATA.value}/{device_name}.pkl", "wb") as pickle_file:
                pickle.dump(id_db, pickle_file)
            raise SystemExit(
                f"Word ids for device '{device_name}' files initially dumped. "
                f"Restart the program."
            )


if __name__ == "__main__":

    db_getter = KindleDBProcessor(
        device_name="Kindle",
        dump_ids=True,
        only_allow_unique_ids=True,
        vocab_key_reference=[],
        initial_id_dump=True,
    )
    print(db_getter.process_lookups())
