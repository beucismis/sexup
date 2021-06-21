import os
import pytest
from backupill import *


this_dir, this_filename = os.path.split(__file__)


def test_generate_backup():
    generate_backup(asc_file=os.path.join(this_dir, "test.asc"))
