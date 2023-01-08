import logging
import subprocess
import time

from app_util.utilities import EJECT_KINDLE
from app.vocab_extractor import main_program
from app_util.import_deck_to_anki import import_deck


def device_checker(device_name: str )-> None:
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

    import_deck(device_name)
    print(data_imported)
    logging.info(data_imported)
    time.sleep(5)

    subprocess.run(EJECT_KINDLE)
    logging.info(unmounted)