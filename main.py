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
from constants import (
    LOG_FILE_NAME,
    time_stamp,
    Configs,
)
from device_system_manager.device_detector import analyze_kindle_vocab_data
from device_system_manager.folder_manager import clear_log_files, clear_results_files


# The working directory must be the directory of the project
os.chdir(Configs.WORKING_DIRECTORY.value)

# Set up logger
logging.basicConfig(
    format="%(asctime)s %(message)s",
    filemode="w",
    filename=LOG_FILE_NAME,
    datefmt="%m/%d/%Y %I:%M:%S %p",
    level=logging.INFO,
)
print(f"{time_stamp}: Main script started running.")

while True:
    timestamp_str = datetime.now().strftime("%m_%d_%Y_%I_%M_%S_%p")
    with open(Configs.KINDLE_PAPER_WHITE_VOCAB_FILE.value, "rb") as out:
        KINDLE_PAPER_WHITE_VOCAB_FILE_ID = pickle.load(out)

    with open(Configs.KINDLE_OASIS_VOCAB_FILE.value, "rb") as out:
        KINDLE_OASIS_VOCAB_FILE_ID = pickle.load(out)

    vocab_key_reference = KINDLE_PAPER_WHITE_VOCAB_FILE_ID + KINDLE_OASIS_VOCAB_FILE_ID

    output = subprocess.run(
        ["system_profiler", "SPUSBDataType"], capture_output=True
    ).stdout.decode()
    KINDLE_MOUNT = os.path.ismount("/Volumes/Kindle")

    # Oasis
    if Configs.SC_KINDLE_OASIS.value in output and KINDLE_MOUNT:
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
    elif Configs.SC_PAPER_WHITE.value in output and KINDLE_MOUNT:
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
        msg = "No Kindle device connected."
        typer.secho(f"{timestamp_str}: {msg}", fg=typer.colors.BRIGHT_BLUE)
        logging.info(msg)
        time.sleep(1)
