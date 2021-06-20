import os
import click
import backupill as bp


@click.argument("file", required=True)
@click.version_option(version=bp.__version__)
@click.command(context_settings=dict(help_option_names=["-h", "--help"]))
def main(file):
    """
    \b
    Generates barcoded PDF to backup text files on paper.
    Source: https://github.com/beucismis/backupill
    """

    if file:
        if not os.path.isfile(file):
            click.echo("Error: File '{}' not found!".format(file))
            exit()

        bp.generate_backup(file)
        click.echo("Done!")
    else:
        click.echo("Usage: packupill FILENAME.asc")


if __name__ == "__main__":
    main()
