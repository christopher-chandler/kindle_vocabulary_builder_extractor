# Standard
import glob
import os
import shutil
import subprocess

# Pip
import typer


# Custom
# None


def generate_sphinx_documentation() -> None:
    """
    After making changes to the main code,
    run this script in order to update the documentation files that
    will automatically be generated by sphinx.

    :return:

        None
    """

    typer.echo(f"Current working directory: {os.getcwd()}")

    if os.path.exists("docs/_sources"):
        typer.echo("Removing existing _sources directory...")
        shutil.rmtree("docs/_sources")

    if os.path.exists("docs/_static"):
        typer.echo("Removing existing _static directory...")
        shutil.rmtree("docs/_static")
    typer.echo("Running sphinx-apidoc...")
    subprocess.call(["sphinx-apidoc", "-o", ".", ".."])

    typer.echo("Running make html...")
    subprocess.call(["make", "html"])

    typer.echo("Copying HTML files...")
    html_files = glob.glob(f"{os.getcwd()}/_build/html/*.*")

    for file in html_files:
        mv = file.split("/")[-1]
        shutil.copy(src=file, dst=f"{os.getcwd()}/{mv}")


if __name__ == "__main__":
    typer.run(generate_sphinx_documentation)