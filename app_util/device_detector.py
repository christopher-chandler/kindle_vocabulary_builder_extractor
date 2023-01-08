# Standard
import logging
import os
import sqlite3
import subprocess
import time

#Pip
import typer 

# Custom
from app_util.constants import EJECT_KINDLE, WORKING_DIRECTORY
from app.vocab_extractor import main_program
from app_util.anki_deck_importer import import_deck

os.chdir(WORKING_DIRECTORY)


def analyze_kindle_vocab_data(**kwargs)-> None:
    time.sleep(4)
    try:
        device_name = kwargs.get("device_name",None)
        time_stamp = kwargs.get("time_stamp",None)
        dump_ids = kwargs.get("dump_ids",None)
        only_allow_unique_ids = kwargs.get("only_allow_unique_ids",None)

        mounted = f"{device_name} is mounted."
        import_data = f"{device_name} data being imported."
        data_imported = f"{device_name}.apkg deck imported."
        unmounted = f"{device_name} unmounted"
        kindle_ids_dumped = f"{device_name} word ids dumped"

        time.sleep(5)
        typer.secho(f"{time_stamp}: {mounted}",fg=typer.colors.BRIGHT_GREEN)
        logging.info(mounted)

        time.sleep(5)
        typer.secho(f"{time_stamp}: {import_data}", fg=typer.colors.CYAN)
        logging.info(import_data)
        new_notes = main_program(device_name=device_name, dump_ids=dump_ids,
                     only_allow_unique_ids=only_allow_unique_ids)
        time.sleep(5)

        if not dump_ids:

            if new_notes:
                import_deck(device_name)
                typer.secho(f"{time_stamp}: {data_imported}",
                            fg=typer.colors.BRIGHT_MAGENTA)
                logging.info(data_imported)
                time.sleep(5)

            subprocess.run(EJECT_KINDLE)
            logging.info(unmounted)

        else:
            print(kindle_ids_dumped)
            subprocess.run(EJECT_KINDLE)
            logging.info(kindle_ids_dumped)
            time.sleep(5)

    except sqlite3.OperationalError as Error:
        logging.error(Error)

