#!/usr/bin/env python3

from src.analise_thesis.channel_data import ChannelData
from test_.analise_thesis.set_up import SetUp
from unittest.mock import patch
from src.analise_thesis.config import Config


class TestChannelData(SetUp):
    def test_put_data(self):
        with patch('Config') as mock:
            path = mock.return_value
            path.excel_spreadsheet_path.return_value = ''
            channel_data = ChannelData(channel_width=896)
            print(str(channel_data))


# if __name__ == '__main__':
#     SetUp.unittest.main()
