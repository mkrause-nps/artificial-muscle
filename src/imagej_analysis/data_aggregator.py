#!/usr/bin/env python3
import statistics

from src.imagej_analysis.channel import Channel, Orientation, Material
from src.imagej_analysis.constants import Constants


class DataAggregator:

    def __init__(self, channels: list[Channel], material: Material, orientation: Orientation):
        self.material = material
        self.orientation = orientation
        self.data: list[Channel] = self.__get_data(channels)

    def __get_data(self, channels: list[Channel]) -> list[Channel]:
        """Returns a filtered list of channels with the given channel width, orientation, and material."""
        return [channel for channel in channels if
                channel.material == self.material and channel.orientation == self.orientation]

    def averages_width(self) -> list:
        """Calculates the average width for each planned width."""
        averages: list[float] = []
        for width in Constants.WIDTHS:
            x_bar_width = [average_data.get_average_width() for average_data in self.data if
                           average_data.planned_width == width]
            x_bar_width = sum(x_bar_width) / len(x_bar_width)
            averages.append(x_bar_width)

        return averages

    def stdevs_width(self) -> list:
        """Calculates the standard deviation for each planned width."""
        stdevs: list[float] = []
        for width in Constants.WIDTHS:
            x_bar_width = [average_data.get_stdev_width() for average_data in self.data if
                           average_data.planned_width == width]
            x_bar_width = sum(x_bar_width) / len(x_bar_width)
            stdevs.append(x_bar_width)

        return stdevs

    def averages_height(self) -> list:
        """Calculates the average width for each planned width."""
        averages: list[float] = []
        for width in Constants.WIDTHS:
            x_bar_height = [average_data.get_average_height() for average_data in self.data if
                            average_data.planned_width == width]
            x_bar_height = sum(x_bar_height) / len(x_bar_height)
            averages.append(x_bar_height)

        return averages

    def stdevs_height(self) -> list:
        """Calculates the standard deviation for each planned width."""
        stdevs: list[float] = []
        for width in Constants.WIDTHS:
            x_bar_height = [average_data.get_stdev_height() for average_data in self.data if
                            average_data.planned_width == width]
            x_bar_height = sum(x_bar_height) / len(x_bar_height)
            stdevs.append(x_bar_height)

        return stdevs

    def get_aspect_ratio(self, width: int) -> list[float]:
        """Returns the aspect ratio for a given planned width."""
        return [average_data.get_average_aspect_ratio() for average_data in self.data if
                average_data.planned_width == width]

    def average_aspect_ratio(self) -> tuple[list, list]:
        """Calculates the mean and standard deviation of the aspect ratio for each planned width."""
        means: list[float] = []
        stdevs: list[float] = []
        for width in Constants.WIDTHS:
            x_ratio = self.get_aspect_ratio(width)
            x_bar_ratio = sum(x_ratio) / len(x_ratio)
            means.append(x_bar_ratio)
            x_stdev_ratio = statistics.stdev(x_ratio)
            stdevs.append(x_stdev_ratio)

        return means, stdevs

    def __len__(self):
        """Defines custom length calculation of a Channel object."""
        return len(self.data)
