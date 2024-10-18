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
from kindle_lex.anki_kindle.kindle.kindle_pickle import KindlePickle as Kp


# Logger
from kindle_lex.settings.logger.basic_logger import catch_and_log_info

# The working directory must be the directory of the project
os.chdir(Gp.WORKING_DIRECTORY.value)

WAIT_TIME = 3
from settings_manager import set_working_directory

# Write the current working directory to the config yaml file
# before the main program starts
set_working_directory()

from kindle_lex.settings.constants.natural_order_group import NaturalOrderGroup


main_app = typer.Typer(
    no_args_is_help=True,
    name="KindleLex",
    add_completion=False,
    cls=NaturalOrderGroup,
)


@main_app.command(name="start", help="start the kindlelex app")
def start_kindlelex(
        initial_id_dump: bool = typer.Option(False, "--dump", "-d",
                                             help="Dump IDS")
) -> None:
    """
    This is the main entry point of the program. Executing this function starts
    the program so that  it can run in the background.
    It listens for connected kindle devices by searching for the devices registered
    in the settings.yaml file.

    Continuously monitors for connected Kindle devices and extracts vocabulary data
        when detected.

        This script runs in an infinite loop, checking for the presence of Kindle devices
        and extracting vocabulary data when a Kindle device is connected.
        The extracted data is analyzed and logged.

        Note:
        - The script runs indefinitely until manually stopped.
        - Result and log files are cleared before each extraction.

    :return:
        None
    """

    try:
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

                    if initial_id_dump:
                        # Dump IDS for the first time
                        Kp(
                            device_name="te",
                            dump_ids=True,
                            initial_id_dump=True,
                            vocab_pickle=device_name,

                        ).dump_ids_to_pickle()
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

    except KeyboardInterrupt:
        raise SystemExit("Program exited.")


@main_app.command(name="init", help="initialize the KindleLex config file")
def generate_config_file():
    pass


if __name__ == "__main__":
    main_app()
