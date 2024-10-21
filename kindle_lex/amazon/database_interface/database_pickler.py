# Standard
import pickle

# Pip
import typer

# Custom
from kindle_lex.settings.constants.constant_paths import GeneralPaths as Gp
from kindle_lex.settings.logger.basic_logger import (
    catch_and_log_error,
    catch_and_log_info,
)
from kindle_lex.amazon.database_interface.database_processor import DatabaseProcessor


class DatabasePickler(DatabaseProcessor):
    """
    This class handles the serialization (pickling) and deserialization
    (unpickling) of Kindle vocabulary data. It allows dumping word IDs to
    a pickle file and loading the data back for further use.
    """

    def __init__(
        self,
        device_name: str,
        vocab_pickle: str,
        only_allow_unique_ids: bool = True,
        vocab_key_reference: str = None,
        dump_ids: bool = False,
        initial_id_dump: bool = False,
    ):
        """
        Initialize the KindlePickle object with the necessary parameters.

        Args:
            device_name (str): The name of the Kindle device.
            vocab_pickle (str): The pickle file name to load the vocabulary data.
            dump_ids (bool): A flag to indicate if IDs should be dumped to a pickle file.
            initial_id_dump (bool): A flag to indicate if it's an initial dump (exits after dumping).
        """
        super().__init__(
            device_name,
            dump_ids,
            only_allow_unique_ids,
            vocab_key_reference,
            initial_id_dump,
        )
        self.device_name = device_name
        self.vocab_pickle = vocab_pickle
        self.dump_ids = dump_ids
        self.initial_id_dump = initial_id_dump

    def dump_ids_to_pickle(self) -> None:
        """
        Dumps Kindle vocabulary word IDs to a pickle file.

        Dumps the IDs to a specified path based on the constant `Gp.DUMPED_DATA`.
        The method handles both regular dumping and initial dumping, where the
        program exits after the dump to prevent further execution.

        Raises:
            SystemExit: If `initial_id_dump` is True, it will raise SystemExit
                        after the dump to prompt a restart.
        """
        id_db = self.process_lookups().get("id_db")

        # Dump IDs to a pickle file if specified
        if self.dump_ids:
            with open(
                f"{Gp.DUMPED_DATA.value}/{self.device_name}.pkl", "wb"
            ) as pickle_file:
                pickle.dump(id_db, pickle_file)

        # If it's the initial ID dump, the program stops after dumping.
        if self.initial_id_dump:
            with open(
                f"{Gp.DUMPED_DATA.value}/{self.device_name}.pkl", "wb"
            ) as pickle_file:
                pickle.dump(id_db, pickle_file)
            raise SystemExit(
                f"Word ids for device '{self.device_name}' have been initially dumped. "
                f"Please restart the program."
            )

    def get_pickle_data(self) -> list or bool:
        """
        Loads Kindle vocabulary data from a pickle file.

        Returns:
            list: The list of vocabulary data loaded from the pickle file.
            bool: Returns False if the file is not found.

        Raises:
            FileNotFoundError: If the specified pickle file is not found,
            it logs the error and returns False.
        """
        try:
            # Construct the file path from the constant path and the pickle filename
            pickle_vocab_data = f"{Gp.DUMPED_DATA.value}/{self.vocab_pickle}.pkl"

            # Open the pickle file in binary read mode and load the data
            with open(pickle_vocab_data, "rb") as pickle_out_file:
                loaded_pickle_data: list = pickle.load(pickle_out_file)

                catch_and_log_info(
                    custom_message="Kindle data loaded successfully.",
                    echo_msg=False,
                )

                return loaded_pickle_data

        except FileNotFoundError as file_not_found_error:
            # Log and return False if the file is not found
            catch_and_log_error(
                error=file_not_found_error,
                custom_message=f"Pickle file '{self.vocab_pickle}.pkl' not found.",
                echo_color=typer.colors.RED,
                echo_msg=True,
                echo_traceback=True,
            )
            return False


if __name__ == "__main__":
    pass
