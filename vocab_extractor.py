# Standard
import datetime

import logging
import os
import subprocess

# Pip
# None

# Custom
from main import main_program
from app_util.utilities import log_file_name

os.chdir("/Users/christopherchandler/Github/Python/kindle_vocabulary_builder_extractor")
logging.basicConfig(format='%(asctime)s %(message)s', filemode="w", filename=log_file_name,
                            datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.INFO)
while True:
    output = subprocess.run(
        ["system_profiler", "SPUSBDataType"], capture_output=True
    ).stdout.decode()

    # Oasis
    if "G000WM0602110684" in output:
        # Run the script
        message ="Kindle Oasis"

        logging.info(message)

        main_program("kindle_oasis")
        print("Kindle Oasis present")

    elif "G000WM0602110684ff" in output:

        message = "Kindle Paperwhite"
        main_program(message)


    else:
            print("No Kindle present")
            message = "No Kindle present"
            logging.info(message)



