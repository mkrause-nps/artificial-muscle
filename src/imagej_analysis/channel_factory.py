#!/usr/bin/env python3

from src.imagej_analysis.channel import Channel


class ChannelFactory:

    @staticmethod
    def create_channel_length_instances(imagej_data_raw: list[list]):
        pass

    @classmethod
    def __create_channel_instance(cls, imagej_data_raw_item: list) -> Channel:
        return Channel(imagej_data_raw_item)
