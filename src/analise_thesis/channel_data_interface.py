#!/usr/bin/env python3

from abc import ABC, abstractmethod


class ChannelDataInterface(ABC):
    @abstractmethod
    def put_data(self) -> None:
        pass

    @abstractmethod
    def get_data(self) -> tuple[list, list, list] | str:
        pass

    @abstractmethod
    def get_mean(self) -> float:
        pass

    @abstractmethod
    def get_stddev(self) -> float:
        pass
