# Standard
# None

# Pip
import typer

# Custom
from kindle_lex.kindle_extractor import vocab_extractor

from kindle_lex.settings.constants.natural_order_group import NaturalOrderGroup

main_app = typer.Typer(
    no_args_is_help=True,
    name="app",
    add_completion=False,
    cls=NaturalOrderGroup,
)


@main_app.command()
def start():
    try:
        vocab_extractor()
    except KeyboardInterrupt:
        raise SystemExit("Program exited")


@main_app.command(name="init", help="initialize the app settings file")
def config_init():
    pass


if __name__ == "__main__":
    main_app()
