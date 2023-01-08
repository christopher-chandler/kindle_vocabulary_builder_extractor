# Standard
import logging
import os
import subprocess
import time

# Pip
# None

# Custom
from app.vocab_extractor import main_program
from app_util.utilities import LOG_FILE_NAME, WORKING_DIRECTORY, EJECT_KINDLE
from app_util.import_deck_to_anki import import_deck
from app_util.serial_numbers import *

os.chdir(WORKING_DIRECTORY)

logging.basicConfig(
    format="%(asctime)s %(message)s",
    filemode="w",
    filename=LOG_FILE_NAME,
    datefmt="%m/%d/%Y %I:%M:%S %p",
    level=logging.INFO,
)

while True:
    kindle_mounted = os.path.ismount('/Volumes/Kindle')
    output = subprocess.run(
        ["system_profiler", "SPUSBDataType"], capture_output=True
    ).stdout.decode()

    # Oasis
    if SC_KINDLE_OASIS in output:
        # Run the script
        device_name = "kindle_oasis"
        logging.info(device_name)
        main_program(device_name)
        print(device_name)

    elif SC_PAPER_WHITE in output and kindle_mounted:

        def device_checker():
            device_name = "kindle_paperwhite"
            mounted = f"{device_name} is mounted."
            import_data = f"{device_name} data being imported."
            data_imported = f"{device_name}.apkg deck imported."
            unmounted = f"{device_name} unmounted"

            time.sleep(5)
            print(mounted)
            logging.info(mounted)

            time.sleep(5)
            print(import_data)
            logging.info(import_data)
            main_program(device_name)
            time.sleep(5)

            import_deck("kindle_paperwhite")
            print(data_imported)
            logging.info(data_imported)
            time.sleep(5)

            subprocess.run(EJECT_KINDLE)
            logging.info(unmounted)

    else:
        logging.debug("No Kindle present")
        device_name = "No Kindle present"
        logging.info(device_name)