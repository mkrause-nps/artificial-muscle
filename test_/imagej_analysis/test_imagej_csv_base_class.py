#!/usr/bin/env python3
import unittest
import os

from src.amscope_excel_loader import AmScopeExcelLoader
from src.imagej_analysis.channel import Channel, ImageApproach
from src.utilities import Utilities


class TestImageJCsvBaseClass(unittest.TestCase):

    def setUp(self):
        self.test_csv_file = os.path.join(Utilities.get_project_root(),
                                          'test_/imagej_measurement_csv/vp_01_192um_black_4x.csv')
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
        self.channel_imagej = Channel(data=self.expected_output_from_load, image_approach=ImageApproach.IMAGEJ)

        data: list[dict] = AmScopeExcelLoader.load(os.path.join(Utilities.get_project_root(),
                                                                'test_/imagej_analysis/test_data/amscope_test_data.xlsx'))
        self.test_amscope_data = data[28]
        self.channel_amscope = Channel(data=self.test_amscope_data, image_approach=ImageApproach.AMSCOPE)
        # print(self.channel_amscope)
