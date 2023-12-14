#!/usr/bin/env python3
import unittest
import os
from src.channel import Channel
from src.utilities import Utilities


class TestImageJCsvBaseClass(unittest.TestCase):

    def setUp(self):
        filename = os.path.join(Utilities.get_project_root(), 'test_/imagej_measurement_csv/vp_01_192um_black_4x.csv')
        self.test_csv_file = filename  # 'test_/imagej_measurement_csv/vp_01_192um_black_4x.csv'
        self.expected_output_from_load = [
            {'item_number': '1', 'Label': 'vp_01_192um_black_4x.tif', 'Length': '331.436'},
            {'item_number': '2', 'Label': 'vp_01_192um_black_4x.tif', 'Length': '327.391'},
            {'item_number': '3', 'Label': 'vp_01_192um_black_4x.tif', 'Length': '326.497'},
            {'item_number': '4', 'Label': 'vp_01_192um_black_4x.tif', 'Length': '135.059'},
            {'item_number': '5', 'Label': 'vp_01_192um_black_4x.tif', 'Length': '149.121'},
            {'item_number': '6', 'Label': 'vp_01_192um_black_4x.tif', 'Length': '139.058'}]
        self.test_csv_files: list = os.listdir(os.path.join(Utilities.get_project_root(),
                                                            'test_/imagej_measurement_csv/vp'))
        self.expected_output_from_filter_filelist = ['vp_01_608um_white_4x.csv', 'vp_01_512um_white_4x.csv',
                                                     'vp_01_608um_black_4x.csv']
        self.channel_length = Channel(imagej_data=self.expected_output_from_load)
