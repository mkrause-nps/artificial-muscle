#!/usr/bin/env python3

from enum import Enum
import statistics


class MaterialColors(Enum):
    WHITE = 'white'
    BLACK = 'black'


class Material(Enum):
    SUP = 'SUP706B'
    Agilus = 'Agilus 30Black FLX985'


class ImageFilename(Enum):
    VP = 'vp'
    HP = 'hp'


class Orientation(Enum):
    VERTICAL = '0 deg'
    HORIZONTAL = '90 deg'


class Channel:

    NUM_MEASUREMENTS = 3

    def __init__(self, imagej_data: list):
        self.filename: str = imagej_data[0]['Label']
        self.__set_orientation()
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

    def get_average_aspect_ratio(self) -> float:
        return self.get_average_height() / self.get_average_width()

    def get_stdev_aspect_ratio(self) -> float:
        return self.get_stdev_height() / self.get_stdev_width()

    def __set_orientation(self):
        if self.filename.startswith(ImageFilename.VP.value):
            self.orientation: Orientation = Orientation.VERTICAL
        elif self.filename.startswith(ImageFilename.HP.value):
            self.orientation: Orientation = Orientation.HORIZONTAL
        else:
            raise ValueError("First letters of filename not recognized - must 'vp' or 'hp'.")

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
            self.material: Material = Material.SUP
        else:
            self.material: Material = Material.Agilus

    def __str__(self) -> str:
        """String representation of a Channel instance."""
        return (f'\nChannel object:\n'
                f'  file name: {self.filename}\n'
                f'  orientation: {self.orientation.value}\n'
                f'  material: {self.material.value}\n'
                f'  planned width: {self.planned_width} um\n'
                f'  measured width: {round(self.get_average_width(), 1)} um\n'
                f'  measured height: {round(self.get_average_height(), 1)} um\n'
                f'  aspect ratio: {round(self.get_average_aspect_ratio(), 2)}')
