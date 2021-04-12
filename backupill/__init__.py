#!/usr/bin/python3

"""
Copyright (C) 2021- beucismis
This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

import os
import click
from .backuper import Pill


__version__ = "0.1.0"
__license__ = "GPL-3.0"
__author__ = "Adil Gurbuz"
__contact__ = "beucismis@tutamail.com"
__source__ = "https://github.com/beucismis/backupill"
__description__ = "Generates barcoded PDF to backup text files on paper."


@click.version_option(version=__version__)
@click.option("-f", "--file", help="ASC file path.")
@click.command(context_settings=dict(help_option_names=["-h", "--help"]))
def main(file):
    """Generates barcoded PDF to backup text files on paper.
    https://github.com/beucismis/backupill
    """

    if file:
        if not os.path.isfile(file):
            click.echo("File '{}' not found!".format(file))
            exit()

        Pill(asc_file=file).generate_backup()
        click.echo("Done!")
    else:
        click.echo("Usage: packupill -f FILENAME.asc")


if __name__ == "__main__":
    main()
