#!/usr/bin/env python3
import unittest

from src.imagej_analysis.channel import Material
from test_.imagej_analysis.test_imagej_csv_base_class import TestImageJCsvBaseClass
from src.imagej_analysis.channel_factory import ChannelFactory


class TestChannelFactory(TestImageJCsvBaseClass):
    def test_create_channel_length_obj(self):
        channel_length = ChannelFactory._ChannelFactory__create_channel_instance(
            imagej_data_raw_item=self.expected_output_from_load)
        self.assertEqual(channel_length.channel_id, '192')
        self.assertEqual(channel_length.chip_id, 'vp_01')
        self.assertEqual(channel_length.material, Material.Agilus)
        self.assertEqual(channel_length.heights, {'1': '331.436', '2': '327.391', '3': '326.497'})
        self.assertEqual(channel_length.widths, {'4': '135.059', '5': '149.121', '6': '139.058'})
        self.assertEqual(channel_length.planned_width, 192)


if __name__ == '__main__':
    unittest.main()
