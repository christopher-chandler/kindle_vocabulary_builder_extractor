# Standard Library Imports
import logging
import sqlite3
import subprocess
import time

# Third-party Library Imports
import typer

# Custom Imports
from constants import EJECT_KINDLE
from anki_kindle.kindle_vocab_extractor import main_extractor
from anki_kindle.anki_deck_importer import import_deck


def analyze_kindle_vocab_data(**kwargs) -> None:
    """
    Analyze and process Kindle vocabulary data.

    Parameters:
    - kwargs (dict): Keyword arguments controlling the analysis and processing.

    Keyword Arguments:
    - device_name (str): Name of the Kindle device.
    - time_stamp (str): Timestamp for logging purposes.
    - dump_ids (bool): Whether to dump vocabulary IDs to a pickle file.
    - only_allow_unique_ids (bool): Whether to allow only unique vocabulary IDs.
    - vocab_key_reference (list): List of reference vocabulary keys.

    Returns:
    - None

    Notes:
    - This function assumes that the Kindle device is mounted and the necessary configurations are set.
    - The Kindle device will be unmounted after processing.

    Example:
    analyze_kindle_vocab_data(device_name="kindle_device", time_stamp="2023-01-01 12:00:00",
                              dump_ids=True, only_allow_unique_ids=True, vocab_key_reference=[...])
    """
    try:
        device_name = kwargs.get("device_name", None)
        time_stamp = kwargs.get("time_stamp", None)
        dump_ids = kwargs.get("dump_ids", None)
        only_allow_unique_ids = kwargs.get("only_allow_unique_ids", None)
        vocab_key_reference = kwargs.get("vocab_key_reference")

        mounted = f"{device_name} is mounted."
        import_data = f"{device_name} data being imported."
        data_imported = f"{device_name}.apkg deck imported."
        unmounted = f"{device_name} unmounted"
        kindle_ids_dumped = f"{device_name} word ids dumped"

        time.sleep(5)
        typer.secho(f"{time_stamp}: {mounted}", fg=typer.colors.BRIGHT_GREEN)
        logging.info(mounted)

        time.sleep(5)
        typer.secho(f"{time_stamp}: {import_data}", fg=typer.colors.CYAN)
        logging.info(import_data)

        new_notes = main_extractor(
            device_name=device_name,
            dump_ids=dump_ids,
            only_allow_unique_ids=only_allow_unique_ids,
            vocab_key_reference=vocab_key_reference,
        )

        time.sleep(5)

        if new_notes:
            import_deck(device_name)
            typer.secho(
                f"{time_stamp}: {data_imported}", fg=typer.colors.BRIGHT_MAGENTA
            )
            logging.info(data_imported)
            time.sleep(5)

            logging.info(unmounted)
            print(kindle_ids_dumped)

            logging.info(kindle_ids_dumped)
            subprocess.run(EJECT_KINDLE)
            time.sleep(5)

        else:
            subprocess.run(EJECT_KINDLE)
            time.sleep(5)

    except sqlite3.OperationalError as Error:
        logging.error(Error)
