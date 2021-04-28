import os
import click
import backupill


@click.version_option(version=backupill.__version__)
@click.option("-f", "--file", help="ASC (.asc) file path.")
@click.command(context_settings=dict(help_option_names=["-h", "--help"]))
def main(file):
    """
    \b
    Generates barcoded PDF to backup text files on paper.
    Source: https://github.com/beucismis/backupill
    """

    if file:
        if not os.path.isfile(file):
            click.echo("File '{}' not found!".format(file))
            exit()

        backupill.generate_backup(asc_file=file)
        click.echo("Done!")
    else:
        click.echo("Usage: packupill -f FILENAME.asc")


if __name__ == "__main__":
    main()
