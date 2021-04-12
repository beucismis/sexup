import os
import pytest
from backupill import Pill


this_dir, this_filename = os.path.split(__file__)


def test_generate_backup():
    pill = Pill(asc_file=os.path.join(this_dir, "test.asc"))
    pill.generate_backup()
