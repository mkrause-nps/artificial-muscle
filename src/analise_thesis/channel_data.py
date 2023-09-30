#!/usr/bin/env python3
import os.path

import pandas as pd
from src.analise_thesis.loader import Loader
from src.analise_thesis.config import Config
from src.analise_thesis.channel_data_interface import ChannelDataInterface


class ChannelData(ChannelDataInterface):

    def __init__(self, channel_width: int):
        self.__channel_width: int = channel_width
        self.num_injections = None
        self.unit = Config.SI_UNIT
        self.df: pd.DataFrame = self.put_data(
            data_path=self.__get_data_filename(), sheet_name=self.__get_sheet_name())

    def put_data(self, data_path: str, sheet_name: str) -> pd.DataFrame:
        df: pd.DataFrame = Loader.read_data(data_path=data_path, sheet_name=sheet_name)
        injection_number = 1
        print(df.loc[df['column_name'] == self.__compose_chip_name(injection_number=injection_number)])
        return df

    def get_mean(self):
        pass

    def get_stddev(self):
        pass

    def get_data(self):
        pass

    def __get_data_filename(self):
        return os.path.join(Config.excel_spreadsheet_path, Config.spreadsheet_filename)

    def __get_sheet_name(self):
        return Config.spreadsheet_filename

    def __compose_chip_name(self, injection_number):
        return f'{injection_number}-{self.__channel_width}'

    def __str__(self):
        return f'Channel Data: width: {self.__channel_width}'
