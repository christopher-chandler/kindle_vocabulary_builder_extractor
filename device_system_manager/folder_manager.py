# Standard
import logging
import os

# Pip
# None

# Custom
from constants import Configs


def clear_log_files(file_amount: int) -> None:

    clear_files = "Clearing log files."
    process_complete = "Log files cleared."

    print(clear_files)
    logging.info(clear_files)
    log_count = 0
    # Iterate directory
    for path in os.listdir(Configs.LOGGING_RESULTS.value):
        # check if current path is a file
        file_exist: bool = os.path.isfile(
            os.path.join(Configs.LOGGING_RESULTS.value, path)
        )
        if file_exist:
            log_count += 1

    if log_count >= file_amount:
        for path in os.listdir(Configs.LOGGING_RESULTS.value):
            full_path = f"{Configs.LOGGING_RESULTS.value}/{path}"
            os.remove(full_path)

    print(process_complete)
    logging.info(process_complete)


def clear_results_files(clear_results: bool = True):
    clear_files = "Clearing result files."
    process_complete = "Result files cleared."

    print(clear_files)
    logging.info(clear_files)

    if clear_results:
        for path in os.listdir(Configs.CSV_VOCAB_RESULTS.value):

            full_file: str = os.path.join(Configs.CSV_VOCAB_RESULTS.value, path)
            file_exist: bool = os.path.isfile(
                os.path.join(Configs.CSV_VOCAB_RESULTS.value, path)
            )

            if file_exist:
                os.remove(full_file)
        open(f"{Configs.CSV_VOCAB_RESULTS.value}/placeholder", mode="w")

        print(process_complete)
        logging.info(process_complete)
