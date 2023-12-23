#!/usr/bin/env python3
import os.path
import unittest

from src.imagej_analysis.channel import Channel, ImageApproach
from src.imagej_analysis.constants import Constants
from test_.imagej_analysis.test_imagej_csv_base_class import TestImageJCsvBaseClass
from unittest.mock import patch, PropertyMock


class TestChannel(TestImageJCsvBaseClass):

    def test_constructor(self):
        expected = '192'
        observed = self.channel_imagej.channel_id
        self.assertEqual(expected, observed)

        expected = 'vp_01'
        observed = self.channel_imagej.chip_id
        self.assertEqual(expected, observed)

        expected = '192'
        observed = self.channel_amscope.channel_id
        self.assertEqual(expected, observed)

        expected = 'AmScope'
        observed = self.channel_amscope.image_approach.value
        self.assertEqual(expected, observed)

        expected = 'hp-09'
        observed = self.channel_amscope.chip_id
        self.assertEqual(expected, observed)

        expected = 'SUP706B'
        observed = self.channel_amscope.material.value
        self.assertEqual(expected, observed)

        expected = 192
        observed = self.channel_amscope.planned_width
        self.assertEqual(expected, observed)

        expected = {'4': 526.0}
        observed = self.channel_amscope.widths
        self.assertEqual(expected, observed)

    def test_average_height(self):
        expected = 328.4413333333334
        actual = self.channel_imagej.get_average_height()
        self.assertEqual(actual, expected)

    def test_average_width(self):
        expected = 141.07933333333332
        actual = self.channel_imagej.get_average_width()
        self.assertEqual(actual, expected)

    def test_stdev_height(self):
        expected = 2.6316972343590783
        actual = self.channel_imagej.get_stdev_height()
        self.assertEqual(actual, expected)

    def test_stdev_widths(self):
        expected = 7.245640229360925
        actual = self.channel_imagej.get_stdev_width()
        self.assertEqual(actual, expected)


if __name__ == '__main__':
    unittest.main()
