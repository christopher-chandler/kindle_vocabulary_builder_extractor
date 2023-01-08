# Stanard
import subprocess


def import_deck(name: str) -> None:
    filename = (
        f"/Users/christopherchandler/"
        f"Github/Python/"
        f"kindle_vocabulary_builder_extractor/results/{name}.apkg"
    )
    app = "/Applications/Anki 2.1.54.app"
    subprocess.run(["open", "-a", app, filename])
