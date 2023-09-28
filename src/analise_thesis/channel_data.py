#!/usr/bin/env python3

import os
import pandas as pd
from channel_data_base_interface import ChannelDataBaseInterface

class ChannelData(ChannelDataBaseInterface):

    def __init__(self, sample_number: str, channel_width: int):
        self.__sample_number: str = sample_number
        self.__channel_width: int = channel_width
        self.num_injections = None
        self.unit = self.UNIT
        self.data = {}

    def put_data(self, data: list[tuple]):
        [self.__put_data(resistance=resistance, stddev=stddev) for resistance, stddev in data]

    def read_data(self, data_path: str):
        absolute_data_filename = os.path.join(data_path, self.__get_data_filename(data_path=data_path))
        df = pd.read_excel(absolute_data_filename, sheet_name='Hard Channel Data')
        df.fillna(method='ffill')

    def get_mean(self):
        pass

    def get_stddev(self):
        pass

    def get_data(self):
        pass

    def __get_data_filename(self, data_path: str, data_filename: str = None) -> str:
        if not data_filename:
            data_filename = os.listdir(data_path)[0]
        return os.path.join(data_path, data_filename)

    def __put_data(self, resistance: float, stddev: float):
        self.num_injections += 1
        self.data[self.num_injections] = [(resistance, stddev)]
