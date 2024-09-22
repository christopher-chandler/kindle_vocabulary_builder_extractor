# Standard Library Imports
import sqlite3
import subprocess
import time

# Third-party Library Imports
import typer

# Custom Imports
from kindle_lex.settings.constants.constant_vars import EJECT_KINDLE
from kindle_lex.anki_kindle.kindle_vocab_extractor import main_extractor
from kindle_lex.anki_kindle.anki_deck_importer import import_deck

from kindle_lex.settings.logger.basic_logger import (
    catch_and_log_error,
    catch_and_log_info,
)


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

        device_mounted = f"{device_name} is mounted."
        import_data = f"{device_name} data being imported."
        data_imported = f"{device_name}.apkg deck imported."
        device_unmounted = f"{device_name} unmounted."
        kindle_ids_dumped = f"{device_name} word ids dumped."

        time.sleep(5)
        mounting_device = f"{time_stamp}: {device_mounted}"
        catch_and_log_info(
            custom_message=mounting_device,
            echo_msg=True,
            echo_color=typer.colors.BRIGHT_GREEN,
        )
        catch_and_log_info(custom_message=device_mounted, echo_msg=True)

        time.sleep(5)
        data_being_imported = f"{time_stamp}: {import_data}"
        catch_and_log_info(
            custom_message=data_being_imported,
            echo_msg=True,
            echo_color=typer.colors.CYAN,
        )
        catch_and_log_info(custom_message=import_data, echo_color=True)

        new_notes = main_extractor(
            device_name=device_name,
            dump_ids=dump_ids,
            only_allow_unique_ids=only_allow_unique_ids,
            vocab_key_reference=vocab_key_reference,
        )
        time.sleep(5)

        # Kindle Lex checks if there is a difference between the data dumped
        if new_notes:
            import_deck(device_name)
            typer.secho(
                f"{time_stamp}: {data_imported}", fg=typer.colors.BRIGHT_MAGENTA
            )

            catch_and_log_info(
                custom_message=data_imported, echo_msg=True, log_info_message=True
            )
            time.sleep(5)

            catch_and_log_info(
                custom_message=device_unmounted, echo_msg=True, log_info_message=True
            )

            catch_and_log_info(
                custom_message=kindle_ids_dumped, echo_msg=True, log_info_message=True
            )

            subprocess.run(EJECT_KINDLE)
            time.sleep(5)

        else:
            subprocess.run(EJECT_KINDLE)
            time.sleep(5)

    except sqlite3.OperationalError as Error:

        catch_and_log_error(
            custom_message="SQL error", error=Error, kill_if_fatal_error=True
        )
