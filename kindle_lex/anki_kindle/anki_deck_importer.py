# Standard
import subprocess

import typer.colors

# Pip
# None

# Custom
from kindle_lex.settings.constants.constant_paths import GeneralPaths as Gp
from kindle_lex.settings.logger.basic_logger import catch_and_log_info


def import_deck(name: str) -> None:
    """
    Import an Anki deck into the Anki application.

    Parameters:
    - name (str): The name of the Anki deck to import.

    Returns:
    - None

    Notes:
    - This function uses the Anki application specified in the Configs module.
    - The imported deck file should be located in the directory specified by
    Configs.ANKI_VOCAB_RESULTS.
    - If the Anki application is not found or the specified deck file does not exist,
    the function will not raise an exception,
    but the import may not be successful.

    """
    filename = f"{Gp.ANKI_APKG.value}/{name}.apkg"
    anki_app = Gp.ANKI_APP.value
    subprocess.run(["open", "-a", anki_app, filename])
    catch_and_log_info(
        custom_message="The deck is being imported...",
        echo_msg=True,
        echo_color=typer.colors.GREEN,
    )


if __name__ == "__main__":
    pass
