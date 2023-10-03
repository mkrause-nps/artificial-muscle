#!/usr/bin/env python3
import os.path

import pandas as pd
from src.analise_thesis.loader import Loader
from src.analise_thesis.config import Config
from src.analise_thesis.channel_data_interface import ChannelDataInterface


class ChannelData(ChannelDataInterface):

    def __init__(self, chip_type: str, channel_width: int):
        self.__chip_type: str = chip_type
        self.__channel_width: int = channel_width
        self.num_injections = None
        self.unit = Config.SI_UNIT
        self.df: pd.DataFrame = self.put_data(
            data_filename=self.__get_data_filename(), sheet_name=self.__get_sheetname())

    def put_data(self, data_filename: str, sheet_name: str) -> pd.DataFrame:
        df: pd.DataFrame = Loader.read_data(data_path=data_filename, sheet_name=sheet_name)
        injection_number = 1
        column_value = self.__compose_chip_name(injection_number=injection_number)
        #print(df.loc[df[self.COLUMN_NAME] == column_value])
        return df.loc[df[Config.COLUMN_NAME_CHIP] == column_value]

    def get_mean(self):
        return self.df[Config.COLUMN_NAME_AVG_RESISTANCE].mean()

    def get_stddev(self):
        return self.df[Config.COLUMN_NAME_AVG_RESISTANCE].std()

    def get_data(self):
        pass

    @staticmethod
    def __get_data_filename():
        return os.path.join(Config.excel_spreadsheet_path, Config.spreadsheet_filename)

    def __get_sheetname(self) -> str:
        return f'{self.__chip_type.capitalize()}{Config.sheet_name_affix}'

    def __compose_chip_name(self, injection_number):
        return f'{injection_number}-{self.__channel_width}'

    def __str__(self):
        return f'Channel Data: width: {self.__channel_width}'
