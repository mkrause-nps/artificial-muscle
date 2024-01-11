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
    PARALLEL = 'parallel'
    PERPENDICULAR = 'perpendicular'


class ImageApproach(Enum):
    IMAGEJ = 'ImageJ'
    AMSCOPE = 'AmScope'


class Channel:

    NUM_MEASUREMENTS = 3

    def __init__(self, data: list[dict] | dict[str: int | str], image_approach: None | ImageApproach):
        if image_approach is None:
            image_approach = ImageApproach.IMAGEJ
        self.image_approach: ImageApproach = image_approach
        self.__set_channel_id(data=data)
        self.__set_chip_id(data=data)
        self.__set_orientation(data=data)
        self.__set_lengths(data=data)
        self.__set_planned_width(data=data)
        self.__set_material(data=data)

    def get_average_height(self) -> float:
        return sum([float(val) for val in self.heights.values()]) / self.NUM_MEASUREMENTS

    def get_average_width(self) -> float:
        if self.image_approach == ImageApproach.IMAGEJ:
            return sum([float(val) for val in self.widths.values()]) / self.NUM_MEASUREMENTS
        if self.image_approach == ImageApproach.AMSCOPE:
            return self.widths.get('3')

    def get_stdev_height(self) -> float:
        return statistics.stdev([float(val) for val in self.heights.values()])

    def get_stdev_width(self) -> float:
        return statistics.stdev([float(val) for val in self.widths.values()])

    def get_average_aspect_ratio(self) -> float:
        return self.get_average_height() / self.get_average_width()

    def get_stdev_aspect_ratio(self) -> float:
        return self.get_stdev_height() / self.get_stdev_width()

    def __set_channel_id(self, data: list[dict] | dict[str: int | str]):
        """Get channel ID from the image file name."""
        if self.image_approach == ImageApproach.IMAGEJ:
            self.channel_id: str = data[0]['Label'][6:9]
        elif self.image_approach == ImageApproach.AMSCOPE:
            self.channel_id: str = str(data.get('channel_id'))

    def __set_chip_id(self, data: list[dict] | dict[str: int | str]):
        """Get chip ID from the image file name."""
        if self.image_approach == ImageApproach.IMAGEJ:
            self.chip_id: str = data[0]['Label'][:5]
        elif self.image_approach == ImageApproach.AMSCOPE:
            self.chip_id: str = data.get('chip_id')

    def __set_orientation(self, data: list[dict] | dict[str: int | str]):
        if self.image_approach == ImageApproach.IMAGEJ:
            if data[0]['Label'].startswith(ImageFilename.VP.value):
                self.orientation: Orientation = Orientation.VERTICAL
            elif data[0]['Label'].startswith(ImageFilename.HP.value):
                self.orientation: Orientation = Orientation.HORIZONTAL
            else:
                raise ValueError("First letters of filename not recognized - must 'vp' or 'hp'.")
        elif self.image_approach == ImageApproach.AMSCOPE:
            if data.get('print_direction') == Orientation.PARALLEL.value:
                self.orientation: Orientation = Orientation.VERTICAL
            elif data.get('print_direction') == Orientation.PERPENDICULAR.value:
                self.orientation: Orientation = Orientation.HORIZONTAL

    def __set_lengths(self, data: list | dict[str: int | str]) -> None:
        if self.image_approach == ImageApproach.IMAGEJ:
            self.heights: dict = {
                data[0]['item_number']: data[0]['Length'],
                data[1]['item_number']: data[1]['Length'],
                data[2]['item_number']: data[2]['Length']
            }

            self.widths: dict = {
                data[3]['item_number']: data[3]['Length'],
                data[4]['item_number']: data[4]['Length'],
                data[5]['item_number']: data[5]['Length']
            }
        elif self.image_approach == ImageApproach.AMSCOPE:
            self.heights: dict = {}
            self.widths: dict = {'4': float(data.get('widths_um'))}

    def __set_planned_width(self, data: list[dict] | dict[str: int | str]) -> None:
        """Set channel planned width."""
        if self.image_approach == ImageApproach.IMAGEJ:
            self.planned_width = int(data[0]['Label'][6:9])
        elif self.image_approach == ImageApproach.AMSCOPE:
            self.planned_width = int(data.get('channel_id'))

    def __set_material(self, data: list[dict] | dict[str: int | str]) -> None:
        """Set channel material."""
        if self.image_approach == ImageApproach.IMAGEJ:
            if MaterialColors.WHITE.value in data[0]['Label']:
                self.material: Material = Material.SUP
            else:
                self.material: Material = Material.Agilus
        elif self.image_approach == ImageApproach.AMSCOPE:
            if data.get('material') == 'sacrificial_material':
                self.material: Material = Material.SUP
            elif data.get('material') == 'black_material':
                self.material = Material.Agilus

    def __str__(self) -> str:
        """String representation of a Channel instance."""
        if self.image_approach == ImageApproach.IMAGEJ:
            return (f'\nChannel object:\n'
                    f'  image approach: {self.image_approach.value}\n'
                    f'  channel ID: {self.channel_id}\n'
                    f'  chip ID: {self.chip_id}'
                    f'  orientation: {self.orientation.value}\n'
                    f'  material: {self.material.value}\n'
                    f'  planned width: {self.planned_width} um\n'
                    f'  measured width: {round(self.get_average_width(), 1)} um\n'
                    f'  measured height: {round(self.get_average_height(), 1)} um\n'
                    f'  aspect ratio: {round(self.get_average_aspect_ratio(), 2)}')
        elif self.image_approach == ImageApproach.AMSCOPE:
            return (f'\nChannel object:\n'
                    f'  image approach: {self.image_approach.value}\n'
                    f'  channel ID: {self.channel_id}\n'
                    f'  chip ID: {self.chip_id}'
                    f'  orientation: {self.orientation.value}\n'
                    f'  material: {self.material.value}\n'
                    f'  planned width: {self.planned_width} um\n'
                    f'  measured width: {round(self.get_average_width(), 1)} um\n')