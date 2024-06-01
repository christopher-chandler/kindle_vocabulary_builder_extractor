# Standard Library Imports
import os

# Custom Imports
from kindle_lex.settings.constants.constant_paths import GeneralPaths as Gp
from kindle_lex.settings.logger.basic_logger import (
    catch_and_log_error,
    catch_and_log_info,
)


def clear_log_files(file_amount: int) -> None:
    """
    Clear log files in the specified directory.

    Parameters:
    - file_amount (int): The maximum number of log files to keep.

    Returns:
    - None

    Notes:
    - This function clears log files in the directory specified by Gp.LOGGING_RESULTS.
    - If the number of log files exceeds the specified limit (file_amount),
      the function removes the excess files, keeping the most recent ones.
    """
    clear_files = "Clearing log files."
    process_complete = "Log files cleared."

    catch_and_log_info(custom_message=clear_files, echo_msg=True)
    log_count = 0

    # Iterate over files in the directory
    for path in os.listdir(Gp.LOGGING_RESULTS.value):
        file_exist: bool = os.path.isfile(os.path.join(Gp.LOGGING_RESULTS.value, path))
        if file_exist:
            log_count += 1

    # Remove excess log files if the count exceeds the specified limit
    if log_count >= file_amount:
        for path in os.listdir(Gp.LOGGING_RESULTS.value):
            full_path = f"{Gp.LOGGING_RESULTS.value}/{path}"
            os.remove(full_path)

    catch_and_log_info(custom_message=process_complete, echo_msg=True)


def clear_results_files(clear_results: bool = True) -> None:
    """
    Clear result files in the specified directory.

    Parameters:
    - clear_results (bool): Whether to clear result files. Defaults to True.

    Returns:
    - None

    Notes:
    - This function clears result files in the directory specified by Gp.ANKI_VOCAB_RESULTS.
    - If clear_results is set to True, the function removes all result files and
    creates a placeholder file.
    """
    clear_files = "Clearing result files."
    process_complete = "Result files cleared."

    catch_and_log_info(custom_message=clear_files, echo_msg=True)

    if clear_results:

        for path in os.listdir(Gp.CSV_VOCAB_RESULTS.value):
            full_file: str = os.path.join(Gp.CSV_VOCAB_RESULTS.value, path)
            file_exist: bool = os.path.isfile(full_file)

            # Remove result files
            if file_exist:
                os.remove(full_file)

        # Create a placeholder file
        open(f"{Gp.CSV_VOCAB_RESULTS.value}/placeholder", mode="w")

        catch_and_log_info(custom_message=process_complete, echo_msg=True)


def open_template(template: str) -> str:
    """
    Opens a text file containing an Anki card template (html and css)
     and returns its content as a string.

    This function is designed to be used with Anki card templates,
    which are plain text files defining the structure of flashcards within the
    Anki spaced repetition software.

    Args:
        template (str): The path to the template file.

    Returns:
        str: The content of the template file.

    Raises:
        IOError: If the template file cannot be opened.
    """
    try:
        with open(template, mode="r") as template_file:
            return template_file.read()
    except FileNotFoundError as error:
        catch_and_log_error(
            error=error,
            echo_msg=True,
            echo_traceback=True,
            custom_message=f"Template file {template} could not be found.",
        )
        return False
