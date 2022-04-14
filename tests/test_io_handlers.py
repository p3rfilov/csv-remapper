
import os
import unittest
import shutil
import uuid

# setup test environment
os.environ['CSV_SETTINGS_DIR'] = os.path.join(os.path.dirname(__file__), 'temp_app_data')

from csv_remapper.components import io_handlers
from csv_remapper.constants import *

ROOT = os.environ['CSV_SETTINGS_DIR']


def setup():
    if not os.path.isdir(ROOT):
        os.makedirs(ROOT)


def cleanup():
    if os.path.isdir(ROOT):
        shutil.rmtree(ROOT)


class TestAppDirectoryHandler(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.handler = io_handlers.AppDirectoryHandler()

    @classmethod
    def tearDownClass(cls):
        cleanup()

    def test_init_folders(self):
        if os.path.isdir(ROOT):
            shutil.rmtree(ROOT)
        self.handler.init_folders()
        self.assertEqual({INPUT_K, OUTPUT_K}, set(os.listdir(ROOT)))

    def test_write_get_settings(self):
        self.handler.write_settings(TEMPLATE_ROOT_DIR_K, ROOT)
        root = self.handler.get_settings(TEMPLATE_ROOT_DIR_K)
        self.assertEqual(ROOT, root)

    def test_is_name_unique(self):
        self.handler.create_template_folder('IN_Test1', INPUT_K)
        self.handler.create_template_folder('OUT_Test2', OUTPUT_K)
        self.handler.create_alias_folder('ALIAS_Test3', OUTPUT_K)
        self.assertTrue(self.handler.is_name_unique('Test'))
        self.assertFalse(self.handler.is_name_unique('IN_Test1'))
        self.assertFalse(self.handler.is_name_unique('OUT_Test2'))
        self.assertFalse(self.handler.is_name_unique('ALIAS_Test3'))


class TestFileHandlers(unittest.TestCase):
    @classmethod
    def tearDownClass(cls):
        cleanup()

    def setUp(self):
        setup()

    def test_csv_read_write(self):
        headers = ['1', '2', '3', '4', '5']
        values = [{h: str(uuid.uuid4()) for h in headers} for i in range(100)]
        test_data = {HEADERS_K: headers, DATA_K: values}
        test_file = os.path.join(ROOT, 'test.csv')
        io_handlers.CsvFileHandler.write(test_file, test_data)
        csv_data = io_handlers.CsvFileHandler.read(test_file)
        self.assertEqual(test_data, csv_data)

    def test_json_read_write(self):
        test_data = {'data': {str(k): str(uuid.uuid4()) for k in range(10)}}
        test_file = os.path.join(ROOT, 'test.json')
        io_handlers.JsonFileHandler.write(test_file, test_data)
        json_data = io_handlers.JsonFileHandler.read(test_file)
        self.assertEqual(test_data, json_data)


if __name__ == '__main__':
    unittest.main()

