#!/usr/bin/env python3

import pandas as pd
from src.analise_thesis.loader import Loader
from src.analise_thesis.config import Config, ChipType
from src.analise_thesis.channel_data import ChannelData


class ChannelDataFactory:
    def __init__(self, chip_type: str, channel_width: int):
        self.chip_type: str = Config.chip_type_selector.get(chip_type)
        self.channel_width: int = channel_width
        self.data_path: str = Config.excel_spreadsheet_path
        self.sheet_name: str = self.__get_sheet_name()

    def generate_channel_data_objects(self):
        return ChannelData(channel_width=self.channel_width)

    def __get_sheet_name(self) -> str:
        return f'{self.chip_type.capitalize()}{Config.sheet_name_affix}'
