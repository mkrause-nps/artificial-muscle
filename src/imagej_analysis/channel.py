#!/usr/bin/env python3

from enum import Enum
import statistics


class MaterialColors(Enum):
    WHITE = 'white'
    BLACK = 'black'


class Material(Enum):
    SUP = 'SUP706B'
    Agilus = 'Agilus 30Black FLX985'


class Channel:

    NUM_MEASUREMENTS = 3

    def __init__(self, imagej_data: list):
        self.filename: str = imagej_data[0]['Label']
        self.__set_lengths(imagej_data)
        self.__set_planned_width()
        self.__set_material()

    def get_average_height(self) -> float:
        return sum([float(val) for val in self.heights.values()]) / self.NUM_MEASUREMENTS

    def get_average_width(self) -> float:
        return sum([float(val) for val in self.widths.values()]) / self.NUM_MEASUREMENTS

    def get_stdev_height(self) -> float:
        return statistics.stdev([float(val) for val in self.heights.values()])

    def get_stdev_width(self) -> float:
        return statistics.stdev([float(val) for val in self.widths.values()])

    def get_channel_side_length_ratio(self) -> float:
        return self.get_average_height()/self.get_average_width()

    def __set_lengths(self, imagej_data: list) -> None:
        self.heights: dict = {
            imagej_data[0]['item_number']: imagej_data[0]['Length'],
            imagej_data[1]['item_number']: imagej_data[1]['Length'],
            imagej_data[2]['item_number']: imagej_data[2]['Length']
        }

        self.widths: dict = {
            imagej_data[3]['item_number']: imagej_data[3]['Length'],
            imagej_data[4]['item_number']: imagej_data[4]['Length'],
            imagej_data[5]['item_number']: imagej_data[5]['Length']
        }

    def __set_planned_width(self) -> None:
        """Extract planned width from file name."""
        self.planned_width = int(self.filename[6:9])

    def __set_material(self) -> None:
        """Set material from color in file name."""
        if MaterialColors.WHITE.value in self.filename:
            self.material: str = Material.SUP.value
        else:
            self.material: str = Material.Agilus.value

    def __str__(self) -> str:
        """String representation of a Channel instance."""
        return (f'\nChannel object:\n'
                f'  file name: {self.filename}\n'
                f'  material: {self.material}\n'
                f'  planned width: {self.planned_width} um\n'
                f'  measured width: {round(self.get_average_width(), 1)} um\n'
                f'  measured height: {round(self.get_average_height(), 1)} um\n'
                f'  aspect ratio: {round(self.get_channel_side_length_ratio(), 2)}')
