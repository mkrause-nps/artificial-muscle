#!/usr/bin/env python3
import os.path
import unittest
import pandas as pd
from src.channel_amscope import ChannelAmScope
from src.config import Config


class TestChannelAmScope(unittest.TestCase):

    def setUp(self):
        self.data: pd.DataFrame = pd.read_json(os.path.join(Config.TEST_DIR, 'amscope_test_data.json'))
        self.single_channel = self.data.loc[
            (self.data['print_direction'] == 'parallel') &
            (self.data['material'] == 'sacrificial_material') &
            (self.data['channel_id'] == 288) &
            (self.data['status'] == 'past')
            ]

    def test_constructor(self):
        channel = ChannelAmScope(data=self.single_channel)
        print(channel)
        self.assertEqual('AmScope', channel.image_approach.value)
        self.assertEqual(288, channel.channel_id)
        self.assertEqual('hp-01', channel.chip_id)
        self.assertEqual('parallel', channel.orientation.value)
        self.assertEqual('SUP706B', channel.material.value)
        self.assertEqual(288, channel.planned_width)

    def test_get_average_width(self):
        channel = ChannelAmScope(data=self.single_channel)
        actual = channel.get_average_width()
        expected = 601.3
        self.assertEqual(expected, actual)

    def test_get_stdev_width(self):
        channel = ChannelAmScope(data=self.single_channel)
        actual = channel.get_stdev_width()
        expected = 35.556059024213205
        self.assertEqual(expected, actual)


if __name__ == '__main__':
    unittest.main()
