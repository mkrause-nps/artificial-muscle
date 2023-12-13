#!/usr/bin/env python3
import unittest
from test_.analise_thesis.set_up import SetUp
from unittest.mock import patch, PropertyMock
from src.analise_thesis.channel_data import ChannelData
from src.analise_thesis.plotter import Plotter


class TestPlotter(SetUp):

    def test_filter_by_width(self):
        data_from_single_channel_width = self.plotter_test.filter_by_width(width=100)
        expected = [(100, 1, 'hard'), (100, 2, 'hard'), (100, 3, 'hard')]
        self.assertEqual(expected, data_from_single_channel_width)

    def test_get_channel_list(self):
        channels = self.plotter_test.get_channel_list()
        expected = [100, 200]
        self.assertEqual(expected, channels)

    @patch('src.analise_thesis.config.Config.spreadsheet_filename', new_callable=PropertyMock,
           return_value='test_data.xlsx')
    @patch('src.analise_thesis.channel_data.ChannelData._ChannelData__get_sheetname')
    @patch('src.analise_thesis.config.Config.excel_spreadsheet_path', new_callable=PropertyMock)
    def test_aggregate_ydata_yerr_from_one_channel(self, mock_path, mock_get_sheetname, mock_spreadsheet_name):
        """Test whether all lists in a tuple (which is from a list of tuples) are of same length"""
        # Some setup work:
        mock_path.return_value = self.test_data_path
        mock_get_sheetname.return_value = 'Foo Bar Data1'
        channel_data = [ChannelData(chip_type='hard', chip_id=1, channel_width=896),
                        ChannelData(chip_type='hard', chip_id=1, channel_width=764),
                        ChannelData(chip_type='hard', chip_id=4, channel_width=192)]

        # Now testing:
        channel_data_aggregated: list[tuple] = Plotter.aggregate_from_one_channel(
            channel_data=channel_data)
        observed = [
            (len(channel_data_aggregated[1][0][0]) == len(channel_data_aggregated[1][0][1]),
             len(channel_data_aggregated[1][1][0]) == len(channel_data_aggregated[1][1][1]),
             len(channel_data_aggregated[1][2][0]) == len(channel_data_aggregated[1][2][1]))
        ]
        self.assertTrue(all(observed))

    def test_get_averaged_channel_data(self):
        pass


if __name__ == '__main__':
    unittest.main()
