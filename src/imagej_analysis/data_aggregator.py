#!/usr/bin/env python3
from typing import List

from src.imagej_analysis.channel import Channel, Orientation, Material
from src.imagej_analysis.constants import Constants
from src.utilities import Utilities
import os


class DataAggregator:
    WIDTHS: List[int] = [192, 288, 384, 512, 608, 704, 800, 896, 992]

    def __init__(self, channels: list[Channel], material: Material, orientation: Orientation):
        self.material = material
        self.orientation = orientation
        self.data: list[Channel] = self.__get_data(channels)

    def __get_data(self, channels: list[Channel]) -> list[Channel]:
        """Returns a filtered list of channels with the given channel width, orientation and material."""
        return [channel for channel in channels if
                channel.material == self.material and channel.orientation == self.orientation]

    def averages_width(self):
        """Calculates the average width for each planned width."""
        averages: list[float] = []
        for width in self.WIDTHS:
            x_bar_width = [average_data.get_average_width() for average_data in self.data if
                           average_data.planned_width == width]
            x_bar_width = sum(x_bar_width) / len(x_bar_width)
            averages.append(x_bar_width)

        return averages

    def stdevs_width(self):
        """Calculates the standard deviation for each planned width."""
        stdevs: list[float] = []
        for width in self.WIDTHS:
            x_bar_width = [average_data.get_stdev_width() for average_data in self.data if
                           average_data.planned_width == width]
            x_bar_width = sum(x_bar_width) / len(x_bar_width)
            stdevs.append(x_bar_width)

        return stdevs

    def averages_height(self):
        """Calculates the average width for each planned width."""
        averages: list[float] = []
        for width in self.WIDTHS:
            x_bar_height = [average_data.get_average_height() for average_data in self.data if
                            average_data.planned_width == width]
            x_bar_height = sum(x_bar_height) / len(x_bar_height)
            averages.append(x_bar_height)

        return averages

    def stdevs_height(self):
        """Calculates the standard deviation for each planned width."""
        stdevs: list[float] = []
        for width in self.WIDTHS:
            x_bar_height = [average_data.get_stdev_height() for average_data in self.data if
                            average_data.planned_width == width]
            x_bar_height = sum(x_bar_height) / len(x_bar_height)
            stdevs.append(x_bar_height)

        return stdevs

    def __len__(self):
        # Define your custom length calculation logic here
        return len(self.data)


if __name__ == '__main__':
    pass
