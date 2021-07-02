import os
import pytest
import backupill as bp


this_dir, this_filename = os.path.split(__file__)
get_test_file = lambda file_name: os.path.join(this_dir, file_name)


def test_generate_backup():
    result = bp.generate_backup(get_test_file("secret_key.asc"))
    assert result == None


def test_restore_backup():
    result = bp.restore_backup(get_test_file("secret_key.asc.pdf"))
    assert result == 0
