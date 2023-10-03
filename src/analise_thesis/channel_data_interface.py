#!/usr/bin/env python3

from abc import ABC, abstractmethod


class ChannelDataInterface(ABC):
    @abstractmethod
    def put_data(self, data_filename: str, sheet_name: str):
        pass

    @abstractmethod
    def get_mean(self):
        pass

    @abstractmethod
    def get_stddev(self):
        pass
