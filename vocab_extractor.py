# Standard

import logging
import os
import subprocess

# Pip
# None

# Custom
from main import main_program
from app_util.utilities import log_file_name
from app_util.import_deck_to_anki import import_deck
from app_util.serial_numbers import *

os.chdir("/Users/christopherchandler/Github/Python/kindle_vocabulary_builder_extractor")
logging.basicConfig(
    format="%(asctime)s %(message)s",
    filemode="w",
    filename=log_file_name,
    datefmt="%m/%d/%Y %I:%M:%S %p",
    level=logging.INFO,
)
while True:
    output = subprocess.run(
        ["system_profiler", "SPUSBDataType"], capture_output=True
    ).stdout.decode()

    # Oasis
    if SC_KINDLE_OASIS in output:
        # Run the script
        message = "kindle_oasis"
        logging.info(message)

        main_program(message)
        import_deck(name=message)
        print("Kindle Oasis is present")

    elif SC_PAPERWHITE in output:
        message = "Kindle Paperwhite"
        main_program(message)

    else:
        print("No Kindle present")
        message = "No Kindle present"
        logging.info(message)