# Stanard
import subprocess

def import_deck(name: str) -> None:
    filename = f'/results/{name}.apkg'
    app = "/Applications/Anki 2.1.54.app"
    subprocess.run(['open', "-a",app, filename])