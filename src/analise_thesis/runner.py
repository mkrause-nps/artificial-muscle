#!/usr/bin/env python3

from src.analise_thesis.config import ChipType
from src.analise_thesis.channel_data_factory import ChannelDataFactory


class Runner:

    @staticmethod
    def create_plots():
        data_obj = ChannelDataFactory(chip_type=ChipType.HARD.name.lower(), channel_width=896)
        data_obj.generate_channel_data_objects()


if __name__ == '__main__':
    Runner.create_plots()
