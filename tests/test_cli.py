
import os
import unittest
import shutil
import glob

# setup test environment
os.environ['CSV_SETTINGS_DIR'] = os.path.join(os.path.dirname(__file__), 'app_data')

from csv_remapper import __main__ as remapper_main
from csv_remapper.constants import *

ROOT = os.path.join(os.path.dirname(__file__), 'temp_data')


class TestCliOperations(unittest.TestCase):
    def setUp(self):
        if not os.path.isdir(ROOT):
            os.makedirs(ROOT)

    def tearDown(self):
        if os.path.isdir(ROOT):
            shutil.rmtree(ROOT)

    def test_run_command(self):
        csv_root = os.path.join(os.path.dirname(__file__), 'csv')
        file1 = os.path.join(csv_root, 'IN_data.csv')
        file2 = os.path.join(csv_root, 'IN_data_copy1.csv')
        file3 = os.path.join(csv_root, 'IN_data_copy2.csv')
        raw_args = [
            '-t', 'Test_Output',
            '-d', ROOT,
            '-f', file1, file2, file3
        ]
        remapper_main.main(raw_args)
        self.assertTrue(1, len(glob.glob(f'{os.path.splitext(file1)[0]}{REMAPPED_SUFFIX}*')))
        self.assertTrue(1, len(glob.glob(f'{os.path.splitext(file2)[0]}{REMAPPED_SUFFIX}*')))
        self.assertTrue(1, len(glob.glob(f'{os.path.splitext(file3)[0]}{REMAPPED_SUFFIX}*')))


if __name__ == '__main__':
    unittest.main()

