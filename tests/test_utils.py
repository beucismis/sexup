import os
import pytest
import backupill as bp


this_dir, this_filename = os.path.split(__file__)
test_file = os.path.join(this_dir, "secret_key.asc")


def test_generate_backup():
    bp.generate_backup(test_file)


def test_restore_backup():
    pass
