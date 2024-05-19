# Standard Library Imports
import logging
import os

# Custom Imports
from kindle_lex.settings.constants.constant_paths import GeneralPaths as Gp


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

    print(clear_files)
    logging.info(clear_files)
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

    print(process_complete)
    logging.info(process_complete)


def clear_results_files(clear_results: bool = True) -> None:
    """
    Clear result files in the specified directory.

    Parameters:
    - clear_results (bool): Whether to clear result files. Defaults to True.

    Returns:
    - None

    Notes:
    - This function clears result files in the directory specified by Gp.CSV_VOCAB_RESULTS.
    - If clear_results is set to True, the function removes all result files and creates a placeholder file.
    """
    clear_files = "Clearing result files."
    process_complete = "Result files cleared."

    print(clear_files)
    logging.info(clear_files)

    if clear_results:
        for path in os.listdir(Gp.CSV_VOCAB_RESULTS.value):
            full_file: str = os.path.join(Gp.CSV_VOCAB_RESULTS.value, path)
            file_exist: bool = os.path.isfile(full_file)

            # Remove result files
            if file_exist:
                os.remove(full_file)

        # Create a placeholder file
        open(f"{Gp.CSV_VOCAB_RESULTS.value}/placeholder", mode="w")

        print(process_complete)
        logging.info(process_complete)
