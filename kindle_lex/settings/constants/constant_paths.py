# Standard
import os
from glob import glob

from enum import Enum

# Pip
# None

# Custom
from kindle_lex.settings.logger.basic_logger import catch_and_log_error
from kindle_lex.settings.messages.message_keys import MessageKeys
from settings_manager import get_config_data


class GeneralPaths(Enum):
    """
    These are hard-coded constants that do not require any special formatting.
    They are drawn from the config.yaml that should be located in the main directory
    of this project.
    """

    # Directories
    WORKING_DIRECTORY = get_config_data().get("WORKING_DIRECTORY")
    LOGGING_RESULTS = get_config_data().get("LOGGING_RESULTS")
    CSV_VOCAB_RESULTS = get_config_data().get("CSV_VOCAB_RESULTS")
    DUMPED_KINDLE_DATA = get_config_data().get("CSV_VOCAB_RESULTS")

    # Anki
    ANKI_APP = get_config_data().get("ANKI_APP")
    ANKI_APKG = get_config_data().get("ANKI_APKG")

    # Anki Templates
    CARD_FRONT_TEMPLATE = "resources/flash_card_templates/front.html"
    CARD_BACK_TEMPLATE = "resources/flash_card_templates/back.html"
    CARD_CSS_TEMPLATE = r"resources/flash_card_templates/style.css"

    # Kindle
    KINDLE_DATABASE = get_config_data().get("KINDLE_DATABASE")
    DUMPED_DATA = get_config_data().get("DUMPED_DATA")

    # Kindle device
    KINDLE_DATABASE_FILE = get_config_data().get("KINDLE_DATABASE_FILE")
    KINDLE_DEVICES = get_config_data().get("KINDLE_DEVICES")

    try:
        """
        The root directory should be defined here,
        so that the following paths are also correct afterwards.
        """

        os.chdir(WORKING_DIRECTORY)

    except Exception as e:
        catch_and_log_error(
            error=e,
            custom_message="N/A",
            kill_if_fatal_error=True,
        )


if __name__ == "__main__":
    pass
