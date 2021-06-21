import pytest
from backupill.cli import main
from click.testing import CliRunner


def test_nothing_found():
    runner = CliRunner()
    result = runner.invoke(main, [""])

    assert result.exit_code == 0
    assert "Usage: packupill FILENAME.asc" in result.output


def test_nothing_file():
    runner = CliRunner()
    result = runner.invoke(main, ["FILENAME.asc"])

    assert result.exit_code == 0
    assert "Error: File 'FILENAME.asc' not found!" in result.output
