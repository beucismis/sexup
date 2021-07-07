import os
import click
import backupill as bp


@click.version_option(version=bp.__version__)
@click.option("--verbose", is_flag=1, help="Will print verbose messages.")
@click.option("-r", "--restore", is_flag=1, help="Restore PDF backup file.")
@click.option("-g", "--generate", is_flag=1, help="Generate PDF backup file.")
@click.argument("filename", type=click.Path(exists=1))
@click.command(context_settings=dict(help_option_names=["--help"]))
def main(generate, restore, verbose, filename):
    """
    \b
    Generates barcoded PDF to backup text files on paper.
    Source: https://github.com/beucismis/backupill

    \b
    Example:
        backupill -g filename.asc
        backupill -r filename.pdf
    """

    if generate and not restore:
        bp.generate_backup(click.format_filename(filename))
        click.echo("Generate backup done!")
    if restore and not generate:
        bp.restore_backup(click.format_filename(filename))
        click.echo("Generate restore done!")


if __name__ == "__main__":
    main()
