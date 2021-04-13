import os
import click
from backupill import __version__


@click.version_option(version=__version__)
@click.option("-f", "--file", help="ASC (.asc) file path.")
@click.command(context_settings=dict(help_option_names=["-h", "--help"]))
def main(file):
    """Generates barcoded PDF to backup text files on paper.
    https://github.com/beucismis/backupill
    """

    if file:
        from backupill import util

        if not os.path.isfile(file):
            click.echo("File '{}' not found!".format(file))
            exit()

        util.generate_backup(asc_file=file)
        click.echo("Done!")
    else:
        click.echo("Usage: packupill -f FILENAME.asc")


if __name__ == "__main__":
    main()
