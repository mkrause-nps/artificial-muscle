#!/usr/bin/env python3

from abc import ABC, abstractmethod

class ChannelDataBaseInterface(ABC):

    @abstractmethod
    def __put_data(self, resistance: float, stddev: float):
        pass

    @abstractmethod
    def put_data(self, data: list):
        pass

    @abstractmethod
    def get_data(self):
        pass

    @abstractmethod
    def get_mean(self):
        pass

    @abstractmethod
    def get_stddev(self):
        pass

    @abstractmethod
    def __get_data_filename(self, data_path: str):
        pass

