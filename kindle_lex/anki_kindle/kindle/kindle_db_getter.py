# Standard
import pickle
import sqlite3

# Custom
import typer

# Standard
from kindle_lex.settings.constants.constant_paths import GeneralPaths as Gp
from kindle_lex.settings.logger.basic_logger import (
    catch_and_log_error,
    catch_and_log_info,
)


class KindleDBGetter:

    def __init__(
        self,
        device_name: str,
        dump_ids: bool,
        initial_id_dump: bool,
        vocab_pickle: str,
    ):
        """
        Keyword Arguments:
        - device_name (str): Name of the Kindle device.
        - dump_ids (bool): Whether to dump vocabulary IDs to a pickle file.



        Returns:
        - bool: True if extraction and processing were successful, False otherwise.
        """

        self.device_name = device_name
        self.dump_ids = dump_ids
        self.initial_id_dump = initial_id_dump
        self.vocab_pickle = vocab_pickle

    @staticmethod
    def __open_kindle_db() -> sqlite3.Cursor:
        """
        When the device is connected to the computer, this opens the kindle database
        saved on that device. It returns a cursor to that devices SQL database so long as
        it is connected.

          Returns:
              sqlite3.Cursor: A cursor object for interacting with the database.
        """

        # Connect to the Kindle vocabulary database
        try:
            vocab_database = sqlite3.connect(Gp.KINDLE_DATABASE.value)
            cursor = vocab_database.cursor()
            return cursor

        except sqlite3.Error as e:

            catch_and_log_error(
                error=e,
                custom_message="The Kindle database could not be opened. This might be "
                "because either the device is not connected, the device "
                "could not be found or the database on the Kindle was "
                "deleted. Please disconnect your device and reconnect it."
                "If this does not resolve the issue, please check the "
                "setting files to see if the path to the Kindle database"
                " was properly specified.",
            )
            raise SystemExit

    def get_book_info(self) -> list:
        """
        Retrieves book information from the BOOK_INFO table.

        Returns:
            list[tuple]: A list of tuples containing book information.
        """

        cursor = self.__open_kindle_db()
        # Retrieve data from BOOK_INFO table
        book_info_cursor = cursor.execute("SELECT * from BOOK_INFO")
        book_info_output = book_info_cursor.fetchall()

        return book_info_output

    def get_lookups(self) -> list:
        """
        Retrieves lookup information from the LOOKUPS table.

        Returns:
            list[tuple]: A list of tuples containing lookup information.
        """
        cursor = self.__open_kindle_db()

        # Retrieve data from LOOKUPS table
        lookup_cursor = cursor.execute("SELECT * from LOOKUPS")
        lookup_cursor_output = lookup_cursor.fetchall()

        return lookup_cursor_output


if __name__ == "__main__":
    db_getter = KindleDBGetter(
        device_name="Kindle",
        dump_ids=True,
    ).get_lookups()
