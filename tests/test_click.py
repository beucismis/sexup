import pytest
from backupill.cli import main
from click.testing import CliRunner


def test_nothing_found():
    runner = CliRunner()
    result = runner.invoke(main, [""])

    assert result.exit_code == 2
