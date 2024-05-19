# Standard
import logging
import os
import pickle
import subprocess
import time

from datetime import datetime

# Pip
import typer

# Custom
from kindle_lex.settings.constants.constant_vars import TIMESTAMP
from kindle_lex.settings.constants.constant_paths import GeneralPaths as Gp

from kindle_lex.device_system_manager.device_detector import analyze_kindle_vocab_data
from kindle_lex.device_system_manager.folder_manager import (
    clear_log_files,
    clear_results_files,
)

# The working directory must be the directory of the project
os.chdir(Gp.WORKING_DIRECTORY.value)

# Set up logger
logging.basicConfig(
    format="%(asctime)s %(message)s",
    filemode="w",
    filename=Gp.LOGGING_RESULTS.value + "/log",
    datefmt="%m/%d/%Y %I:%M:%S %p",
    level=logging.INFO,
)


def vocab_extractor() -> None:
    """
    Continuously monitors for connected Kindle devices and extracts vocabulary data when detected.

    This script runs in an infinite loop, checking for the presence of Kindle devices
    and extracting vocabulary data when a Kindle device is connected. It supports Kindle
    Paper White and Kindle Oasis devices. The extracted data is analyzed and logged.

    Note:
    - The script runs indefinitely until manually stopped.
    - Result and log files are cleared before each extraction.

    Returns:
        None
    """

    print(f"{TIMESTAMP}: Main script started running...")

    while True:
        timestamp_str = datetime.now().strftime("%m_%d_%Y_%I_%M_%S_%p")
        with open(Gp.KINDLE_PAPER_WHITE_VOCAB_FILE.value, "rb") as out:
            KINDLE_PAPER_WHITE_VOCAB_FILE_ID = pickle.load(out)

        with open(Gp.KINDLE_OASIS_VOCAB_FILE.value, "rb") as out:
            KINDLE_OASIS_VOCAB_FILE_ID = pickle.load(out)

        vocab_key_reference = (
            KINDLE_PAPER_WHITE_VOCAB_FILE_ID + KINDLE_OASIS_VOCAB_FILE_ID
        )

        output = subprocess.run(
            ["system_profiler", "SPUSBDataType"], capture_output=True
        ).stdout.decode()
        KINDLE_MOUNT = os.path.ismount("/Volumes/Kindle")

        # Oasis
        if Gp.SC_KINDLE_OASIS.value in output and KINDLE_MOUNT:
            clear_results_files(True)
            clear_log_files(5)
            analyze_kindle_vocab_data(
                device_name="kindle_oasis",
                time_stamp=timestamp_str,
                dump_ids=True,
                only_allow_unique_ids=True,
                vocab_key_reference=vocab_key_reference,
            )

            time.sleep(1)
        elif Gp.SC_PAPER_WHITE.value in output and KINDLE_MOUNT:
            clear_results_files(True)
            clear_log_files(5)
            analyze_kindle_vocab_data(
                device_name="kindle_paper_white",
                time_stamp=timestamp_str,
                dump_ids=True,
                only_allow_unique_ids=True,
                vocab_key_reference=vocab_key_reference,
            )
            time.sleep(1)
        else:
            msg = "No Kindle device connected..."
            typer.secho(f"{timestamp_str}: {msg}", fg=typer.colors.BRIGHT_BLUE)
            logging.info(msg)
            time.sleep(1)


if __name__ == "__main__":
    pass
