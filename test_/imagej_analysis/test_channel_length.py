#!/usr/bin/env python3
import unittest
from test_.imagej_analysis.test_imagej_csv_base_class import TestImageJCsvBaseClass


class TestChannelLength(TestImageJCsvBaseClass):
    def test_average_height(self):
        expected = 328.4413333333334
        actual = self.channel_length.get_average_height()
        self.assertEqual(actual, expected)

    def test_average_width(self):
        expected = 141.07933333333332
        actual = self.channel_length.get_average_width()
        self.assertEqual(actual, expected)

    def test_stdev_height(self):
        expected = 2.6316972343590783
        actual = self.channel_length.get_stdev_height()
        self.assertEqual(actual, expected)

    def test_stdev_widths(self):
        expected = 7.245640229360925
        actual = self.channel_length.get_stdev_width()
        self.assertEqual(actual, expected)


if __name__ == '__main__':
    unittest.main()
