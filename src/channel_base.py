#!/usr/bin/env python3

from abc import ABCMeta, abstractmethod


class ChannelBase(metaclass=ABCMeta):
    @abstractmethod
    def get_average_width(self):
        raise NotImplementedError

    @abstractmethod
    def get_stdev_width(self):
        raise NotImplementedError
