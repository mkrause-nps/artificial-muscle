#!/usr/bin/env python3
import pandas as pd
from statistics import stdev
from src.channel_base import ChannelBase
from src.imagej_analysis.channel import ImageApproach, Orientation, Material


class ChannelAmScope(ChannelBase):
    idx_first_item = 0

    def __init__(self, data: pd.DataFrame):
        super().__init__()
        self.__set_data(data)
        self.image_approach: ImageApproach = ImageApproach.AMSCOPE
        self.channel_id: str = data.iloc[[self.idx_first_item]]['channel_id'].values[0]
        self.chip_id: str = data.iloc[[self.idx_first_item]]['chip_id'].values[0]
        self.planned_width: int = int(self.channel_id)
        self.__set_orientation(data)
        self.__set_material(data)

    def __set_data(self, data: pd.DataFrame) -> None:
        self.data: list[tuple[int, float]] = list(zip(data['chip_id'], data['widths_um']))

    def __set_orientation(self, data: pd.DataFrame) -> None:
        if data.iloc[[self.idx_first_item]]['print_direction'].values[0] == 'perpendicular':
            self.orientation: Orientation = Orientation.HORIZONTAL
        else:
            self.orientation: Orientation = Orientation.VERTICAL

    def __set_material(self, data: pd.DataFrame) -> None:
        if data.iloc[[self.idx_first_item]]['material'].values[0] == ' black_resin':
            self.material: Material = Material.Agilus
        else:
            self.material: Material = Material.SUP

    def get_average_width(self) -> float:
        width = self.__get_width()
        return sum(width) / len(width)

    def get_stdev_width(self) -> float:
        width = self.__get_width()
        return stdev(width)

    def __get_width(self) -> list[float]:
        return [y for (x, y) in self.data]

    def __str__(self) -> str:
        return (f'\nChannel object:\n'
                f'  image approach: {self.image_approach.value}\n'
                f'  channel ID: {self.channel_id}\n'
                f'  chip ID: {self.chip_id}\n'
                f'  orientation: {self.orientation.value}\n'
                f'  material: {self.material.value}\n'
                f'  planned width: {self.planned_width} um\n'
                f'  measured width: {round(self.get_average_width(), 1)} um\n'
                )
