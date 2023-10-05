#!/usr/bin/env python3

import os
import pandas as pd
from src.analise_thesis.loader import Loader
from src.analise_thesis.config import Config
from src.analise_thesis.channel_data_interface import ChannelDataInterface


class ChannelData(ChannelDataInterface):
    """Holds data from a specific channel type and width, and can generate statistical output from it."""

    COLUMN_INJECTION_NUM = 'Injection Number'
    COLUMN_RESISTANCE = 'Resistance (kΩ)'
    COLUMN_STDDEV = 'Standard Deviation (kΩ)'

    def __init__(self, chip_type: str, chip_id: int, channel_width: int):
        self.__chip_type: str = chip_type
        self.__chip_id: int = chip_id
        self.__channel_width: int = channel_width
        self.is_data = False
        self.num_injections = None
        self.unit = Config.SI_UNIT
        self.df: pd.DataFrame = self.put_data()

    def put_data(self) -> pd.DataFrame:
        data_filename = self.__get_data_filename()
        sheet_name = self.__get_sheetname()
        df: pd.DataFrame = Loader.read_data(data_path=data_filename, sheet_name=sheet_name)
        if not df.empty:
            self.is_data = True
        column_value = self.__compose_chip_name(chip_number=self.__chip_id)
        df = df.loc[df[Config.COLUMN_NAME_CHIP] == column_value]
        self.num_injections = len(df.index)

        return df

    def get_data(self) -> tuple[list, list, list] | str:
        if not self.is_data:
            return "contains no data - put data first"
        return (self.df[self.COLUMN_INJECTION_NUM].tolist(),
                self.df[self.COLUMN_RESISTANCE].tolist(),
                self.df[self.COLUMN_STDDEV].tolist())

    def get_mean(self) -> float:
        return self.df[Config.COLUMN_NAME_AVG_RESISTANCE].mean()

    def get_stddev(self) -> float:
        return self.df[Config.COLUMN_NAME_AVG_RESISTANCE].std()

    @staticmethod
    def __get_data_filename():
        return os.path.join(Config.excel_spreadsheet_path, Config.spreadsheet_filename)

    def __get_sheetname(self) -> str:
        return f'{self.__chip_type.capitalize()}{Config.sheet_name_affix}'

    def __compose_chip_name(self, chip_number):
        return f'{chip_number}-{self.__channel_width}'

    def __str__(self):
        return f'Channel Data: width: {self.__channel_width}'
