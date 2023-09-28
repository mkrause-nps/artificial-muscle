#!/usr/bin/env python3

from

class HardChannelData(ChannelDataBaseInterface):

    UNIT = 'kOhm'

    def __init__(self, sample_number: str, channel_width: int):
        self.__sample_number: str = sample_number
        self.__channel_width: int = channel_width
        self.num_injections = None
        self.unit = self.UNIT
        self.data = {}

    def get_mean(self):
        pass

    def get_stddev(self):
        pass

    def get_data(self):
        pass


    def __put_data(self, resistance: float, stddev: float):
        self.num_injections += 1
        self.data[self.num_injections] = [(resistance, stddev)]

    def put_data(self, data: list[tuple]):
        self.data = [self.__put_data(resistance=resistance, stddev=stddev) for resistance, stddev in data]

    def read_data(self):
        pass


if __name__ == '__main__':
    pass
