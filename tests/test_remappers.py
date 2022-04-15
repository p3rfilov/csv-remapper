
import os
import unittest

# setup test environment
os.environ['CSV_SETTINGS_DIR'] = os.path.join(os.path.dirname(__file__), 'app_data')

from csv_remapper.components import io_handlers, datatypes
from csv_remapper.components import remappers


class TestDataRemapping(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.dir_handler = io_handlers.AppDirectoryHandler()
        cls.csv_file_root = os.path.join(os.path.dirname(__file__), 'csv')

    def test_convert_value(self):
        tests = [
            ('test text', datatypes.DataTypes.TEXT, datatypes.DataTypes.TEXT, 'test text'),

            ('1234', datatypes.DataTypes.TEXT, datatypes.DataTypes.NUM_POS, '1234'),
            ('-1234', datatypes.DataTypes.TEXT, datatypes.DataTypes.NUM_POS, '1234'),
            ('1234', datatypes.DataTypes.TEXT, datatypes.DataTypes.NUM_NEG, '-1234'),

            ('2019/08/12', datatypes.DataTypes.TEXT, datatypes.DataTypes.DATE_DMY_S, '12/08/2019'),
            ('2019/08/12', datatypes.DataTypes.TEXT, datatypes.DataTypes.DATE_MDY_S, '08/12/2019'),
            ('2019/08/12', datatypes.DataTypes.TEXT, datatypes.DataTypes.DATE_YMD_S, '2019/08/12'),
            ('2019/08/12', datatypes.DataTypes.TEXT, datatypes.DataTypes.DATE_DMY_H, '12-08-2019'),
            ('2019/08/12', datatypes.DataTypes.TEXT, datatypes.DataTypes.DATE_MDY_H, '08-12-2019'),
            ('2019/08/12', datatypes.DataTypes.TEXT, datatypes.DataTypes.DATE_YMD_H, '2019-08-12'),
            ('2019/08/12', datatypes.DataTypes.TEXT, datatypes.DataTypes.DATE_DMY_D, '12.08.2019'),
            ('2019/08/12', datatypes.DataTypes.TEXT, datatypes.DataTypes.DATE_MDY_D, '08.12.2019'),
            ('2019/08/12', datatypes.DataTypes.TEXT, datatypes.DataTypes.DATE_YMD_D, '2019.08.12'),

            ('12/08/2007', datatypes.DataTypes.DATE_DMY_S, datatypes.DataTypes.DATE_YMD_S, '2007/08/12'),
            ('12/08/2007', datatypes.DataTypes.DATE_MDY_S, datatypes.DataTypes.DATE_YMD_S, '2007/12/08'),
            ('2007/08/12', datatypes.DataTypes.DATE_YMD_S, datatypes.DataTypes.DATE_YMD_S, '2007/08/12'),
        ]
        for val, in_type, out_type, result in tests:
            self.assertEqual(result, remappers._convert_value(val, in_type, out_type))

    def test_extract_substring(self):
        tests = [
            ('john@google.com', '@(.+)\\.', 'google'),
            ('john@google.com', '(.+)@', 'john'),
            ('@google.com', '(.+)@', ''),
        ]
        for val, reg_ex, result in tests:
            self.assertEqual(result, remappers._extract_substring(val, reg_ex))

    def test_remap_with_secondary_data(self):
        csv_in = os.path.join(self.csv_file_root, 'IN_data.csv')
        csv_out = os.path.join(self.csv_file_root, 'OUT_test_expected_output.csv')
        test_out_data = io_handlers.CsvFileHandler.read(csv_out)
        remapped_data = remappers.remap_csv_file(csv_in, 'Test_Output', self.dir_handler)
        self.assertEqual(test_out_data, remapped_data)


if __name__ == '__main__':
    unittest.main()
