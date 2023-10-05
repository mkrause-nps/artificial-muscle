#!/usr/bin/env python3

from src.analise_thesis.channel_data import ChannelData
from test_.analise_thesis.set_up import SetUp
from unittest.mock import patch, PropertyMock


@patch('src.analise_thesis.config.Config.spreadsheet_filename', new_callable=PropertyMock,
       return_value='test_data.xlsx')
@patch('src.analise_thesis.channel_data.ChannelData._ChannelData__get_sheetname')
@patch('src.analise_thesis.config.Config.excel_spreadsheet_path', new_callable=PropertyMock)
class TestChannelData(SetUp):
    def test_constructor(self, mock_path, mock_get_sheetname, mock_spreadsheet_name):
        mock_path.return_value = self.test_data_path
        mock_get_sheetname.return_value = 'Foo Bar Data1'
        channel_data = ChannelData(chip_type='hard', chip_id=1, channel_width=896)
        expected_number_of_rows = 3
        self.assertEqual(len(channel_data.df.index), expected_number_of_rows)
        expected_number_of_columns = 3
        self.assertEqual(len(channel_data.df), expected_number_of_columns)

    def test_get_average(self, mock_path, mock_get_sheetname, mock_spreadsheet_name) -> None:
        mock_path.return_value = self.test_data_path
        mock_get_sheetname.return_value = 'Foo Bar Data1'
        channel_data = ChannelData(chip_type='hard', chip_id=1, channel_width=896)

        expected_avg = 54.50066666666667
        observed_avg = channel_data.get_mean()
        self.assertEqual(expected_avg, observed_avg)

    def test_get_stddev(self, mock_path, mock_get_sheetname, mock_spreadsheet_name) -> None:
        mock_path.return_value = self.test_data_path
        mock_get_sheetname.return_value = 'Foo Bar Data1'
        channel_data = ChannelData(chip_type='hard', chip_id=1, channel_width=896)

        expected_std = 72.77112835000797
        observed_std = channel_data.get_stddev()
        self.assertEqual(expected_std, observed_std)
