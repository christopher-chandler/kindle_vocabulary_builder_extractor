# Standard
# None

# Pip
import typer

# Custom
from kindle_lex.amazon.app_kindle.app import kindle_app

main_app = typer.Typer()

main_app.add_typer(kindle_app, name="kindle")


if __name__ == "__main__":
    kindle_app()
