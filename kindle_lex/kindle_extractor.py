# Standard
import datetime
import os
import subprocess
import time

# Pip
import typer

# Custom

# Constants
from kindle_lex.anki_kindle.main_kindle_vocab_extractor import main_extractor
from kindle_lex.settings.constants.constant_paths import GeneralPaths as Gp
from kindle_lex.settings.constants.constant_vars import TIMESTAMP

# Device
from kindle_lex.device_system_manager.device_detector import analyze_kindle_vocab_data
from kindle_lex.device_system_manager.load_dumped_kindle_data import get_pickle_data
from kindle_lex.device_system_manager.file_manager import (
    clear_log_files,
    clear_results_files,
)

# Logger
from kindle_lex.settings.logger.basic_logger import catch_and_log_info

# The working directory must be the directory of the project
os.chdir(Gp.WORKING_DIRECTORY.value)

WAIT_TIME = 3


def vocab_extractor() -> None:
    """
    Continuously monitors for connected Kindle devices and extracts vocabulary data
    when detected.

    This script runs in an infinite loop, checking for the presence of Kindle devices
    and extracting vocabulary data when a Kindle device is connected.
    The extracted data is analyzed and logged.

    Note:
    - The script runs indefinitely until manually stopped.
    - Result and log files are cleared before each extraction.

    Returns:
        None
    """

    catch_and_log_info(
        custom_message=f"{TIMESTAMP}: Main script started running...",
        echo_msg=True,
        echo_color=typer.colors.BRIGHT_GREEN,
    )
    while True:
        RUN_TIME_TIME_STAMP = datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
        KINDLE_DEVICES = Gp.KINDLE_DEVICES.value

        # Checks if device with the kindle id is connected to the computer
        subprocess_connected_devices_output = subprocess.run(
            ["system_profiler", "SPUSBDataType"], capture_output=True
        ).stdout.decode()
        KINDLE_MOUNT = os.path.ismount("/Volumes/Kindle")

        for device_name in KINDLE_DEVICES:
            device_id = KINDLE_DEVICES.get(device_name)

            if device_id in subprocess_connected_devices_output and KINDLE_MOUNT:
                clear_log_files(5)
                clear_results_files(False)

                kindle_pickle = get_pickle_data(device_name)

                # Dump IDS for the first time
                if kindle_pickle is False:
                    main_extractor(
                        device_name=device_name,
                        initial_id_dump=True,
                    )

                else:
                    analyze_kindle_vocab_data(
                        device_name=device_name,
                        time_stamp=TIMESTAMP,
                        dump_ids=True,
                        only_allow_unique_ids=True,
                        vocab_key_reference=get_pickle_data(device_name),
                    )

                time.sleep(WAIT_TIME)
        else:
            msg = "No Kindle device connected at the moment..."

            catch_and_log_info(
                custom_message=f"{RUN_TIME_TIME_STAMP}: {msg}",
                echo_msg=True,
                echo_color=typer.colors.BRIGHT_BLUE,
            )
            time.sleep(WAIT_TIME)


if __name__ == "__main__":
    pass
