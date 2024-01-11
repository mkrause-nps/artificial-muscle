#!/usr/bin/env python3

from src.imagej_analysis.channel import Channel


class ChannelFactory:

    @classmethod
    def create_channel_length_instances(cls, imagej_data_raw_items: list[list]) -> list[Channel]:
        """Returns a list of channel objects
        :param imagej_data_raw_items: a list of 'imagej_data_raw_item's
        :return: a list of one channel object for each imagej_data_raw_item item
        """
        return list(map(cls.__create_channel_instance, imagej_data_raw_items))

    @classmethod
    def __create_channel_instance(cls, imagej_data_raw_item: list) -> Channel:
        return Channel(data=imagej_data_raw_item, image_approach=None)
