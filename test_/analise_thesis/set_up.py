#!/usr/bin/env python3

import unittest
import os
import pandas as pd
from src.analise_thesis.plotter import Plotter


class SetUp(unittest.TestCase):
    def setUp(self) -> None:
        self.test_data_path: str = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'test_data')
        self.test_data_filename: str = 'test_data.xlsx'
        self.test_data_sheet1_name: str = 'Foo Bar Data1'
        self.test_data_filename_not_exists: str = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'foo.xlsx')
        self.test_json_filename: str = 'exported_dataframe.json'
        self.json_filename: str = os.path.join(self.test_data_path, self.test_json_filename)
        data = {'Product': ['Computer', 'Printer', 'Monitor', 'Tablet', 'Keyboard'],
                'Price': [1200, 200, 500, 350, 80]
                }
        self.df = pd.DataFrame(data)
        data2 = {
            'Chip Name': ['1-896'] * 3 + ['1-764'] * 5 + ['4-192'] * 2,
            'Injection Number': list(range(1, 4)) + list(range(1, 6)) + list(range(1, 3)),
            'Resistance (kΩ)': [138.4, 16.59, 8.512, 225.3, 28.18, 9.743, 8.656, 5.945, 220000, 198.8],
            'Standard Deviation (kΩ)': [0.6969, 0.1366, 0.2016, 0.1587, 0.4957, 0.273, 0.03024, 0.03056, 0, 0.03857]
        }
        self.df2 = pd.DataFrame(data2)

        data_hard = [
            (100, 1, 'hard'),
            (200, 1, 'hard'),
            (100, 2, 'hard'),
            (100, 3, 'hard'),
        ]

        self.plotter_test = Plotter(data=data_hard, nrows=1, ncols=1, xlabel="injection number", ylabel='R [K$\Omega$]',
                                    xlim=[0, 5], ylim=[0, 1e6], aspect=1.0, fontsize=12, fig_format='png', capsize=10)

    def tearDown(self) -> None:
        if self.test_data_path:
            file_to_remove = os.path.join(self.test_data_path, self.test_json_filename)
        if os.path.exists(file_to_remove):
            os.remove(self.json_filename, )  # one test write that file to disk - remove it again


if __name__ == '__main__':
    unittest.main()
