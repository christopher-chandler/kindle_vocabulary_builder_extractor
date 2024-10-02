# Standard library import
import pickle

# Pip
import typer.colors

# Custom
from kindle_lex.settings.constants.constant_paths import GeneralPaths as Gp
from kindle_lex.settings.logger.basic_logger import (
    catch_and_log_error,
    catch_and_log_info,
)


def get_pickle_data(vocab_pickle: str) -> dict:
    """Loads data from a pickle file.

    Args:
        vocab_pickle: The name of the pickle file to load. (str)

    Returns:
        The loaded data from the pickle file. (list)

    Raises:
        FileNotFoundError: If the specified pickle file is not found.
    """

    try:
        # Construct the file path from the constant path and the pickle filename
        pickle_vocab_data: pickle = f"{Gp.DUMPED_DATA.value}/{vocab_pickle}.pkl"

        # Open the pickle file in binary read mode and load the data
        with open(pickle_vocab_data, "rb") as pickle_out_file:
            loaded_pickle_data: list = pickle.load(pickle_out_file)

            catch_and_log_info(
                custom_message="Kindle data loaded",
                echo_msg=True,
            )

            return loaded_pickle_data

    except FileNotFoundError as file_not_found_error:
        # Indicate an error if the file is not found
        catch_and_log_error(
            error=file_not_found_error,
            custom_message=str(file_not_found_error),
            echo_color=typer.colors.RED,
            echo_msg=True,
            echo_traceback=True,
        )
        return False


# Run the function if the script is executed directly
#
if __name__ == "__main__":
    test_pickle = get_pickle_data("SC_KINDLE_OASIS")
    print(test_pickle)
