# Standard
import glob
import os
import shutil
import subprocess

# Pip
import typer


# Custom
# None


def generate_documenation() -> None:
    """
    After making changes to the code, run this script in order to update the documentation
    files.

    :return:
    None
    """
    typer.echo("Running sphinx-apidoc...")
    subprocess.call(["sphinx-apidoc", "-o", ".", ".."])

    typer.echo("Running make html...")
    subprocess.call(["make", "html"])

    # typer.echo("Copying README file from main directory...")
    # shutil.copy(src="/Users/christopherchandler/code_repos/christopher-chandler/Python
    # /kindle_vocabulary_builder_extractor/README.rst", dst=f"{os.getcwd()}/README.rst")

    typer.echo(f"Current working directory: {os.getcwd()}")

    if os.path.exists("_sources"):
        typer.echo("Removing existing _sources directory...")
        shutil.rmtree("_sources")

    if os.path.exists("_static"):
        typer.echo("Removing existing _static directory...")
        shutil.rmtree("_static")

    typer.echo("Copying _sources from _build/html...")
    shutil.copytree(src=f"{os.getcwd()}/_build/html/_sources", dst="_sources")

    typer.echo("Copying _static from _build/html...")
    shutil.copytree(src=f"{os.getcwd()}/_build/html/_static", dst="_static")

    typer.echo("Copying HTML files...")
    html_files = glob.glob(f"{os.getcwd()}/_build/html/*.*")
    for file in html_files:
        mv = file.split("/")[-1]
        shutil.copy(src=file, dst=f"{os.getcwd()}/{mv}")


if __name__ == "__main__":
    typer.run(generate_documenation)
