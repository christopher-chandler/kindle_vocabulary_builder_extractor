# Standard
# None

# Pip
import typer

# Custom
from settings_manager import set_working_directory

# Write the current working directory to the config yaml file
# before the main program starts
set_working_directory()

from kindle_lex.kindle_extractor import vocab_extractor
from kindle_lex.settings.constants.natural_order_group import NaturalOrderGroup

"""
This is the main entry point of KindleLex. 
"""


main_app = typer.Typer(
    no_args_is_help=True,
    name="KindleLex",
    add_completion=False,
    cls=NaturalOrderGroup,
)


@main_app.command(name="start", help="start kindlelex")
def start_kindlelex() -> None:
    """
    This is the main entry point of the program. Executing this function starts
    the program so that  it can run in the background.
    It listens for connected kindle devices by searching for the devices registered
    in the settings.yaml file.

    :return:
        None
    """
    try:
        vocab_extractor()
    except KeyboardInterrupt:
        raise SystemExit("Program exited.")


if __name__ == "__main__":
    main_app()
