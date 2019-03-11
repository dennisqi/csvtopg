import sys
import unittest
import pandas as pd

sys.path.insert(0, '../csvtopg')
from csv_helpers import *


class TestCSVHelpers(unittest.TestCase):
    def test_get_base_filename(self):
        valid_file = './data/loan.csv'
        expected_base_filename = './data/loan'
        self.assertEqual(expected_base_filename, get_base_filename(valid_file))

        invalid_file_type = 1
        with self.assertRaises(TypeError):
            get_base_filename(invalid_file_type)

        invalid_file = './data/loan'
        with self.assertRaises(ValueError):
            get_base_filename(invalid_file)

    def test_convert_to_dt(self):
        null = float('NaN')
        self.assertTrue(pd.isnull(convert_to_dt(null)))

        bY = 'Dec-2018'
        expected_bY = '2018-12-01'
        self.assertEqual(expected_bY, convert_to_dt(bY))

        by = 'Dec-18'
        expected_by = '2018-12-01'
        self.assertEqual(expected_by, convert_to_dt(by))

    def test_get_header(self):
        csv = 'data/test.csv'
        expected_headers = ['header1', 'header2', 'header_3']
        self.assertEqual(expected_headers, get_header(csv))

    def test_read_df_lines(self):
        csv = 'data/test.csv'
        df = pd.read_csv(csv)
        expected = [{'header1': 1, 'header2': 2, 'header_3': 3}]
        result = list(read_df_lines(df))
        self.assertEqual(expected, result)


if __name__ == '__main__':
    unittest.main()
