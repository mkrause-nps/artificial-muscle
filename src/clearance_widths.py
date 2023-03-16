#!/usr/bin/env python3

import os
import numpy as np
import matplotlib.pyplot as plt
import csv
import json
import logging
from scipy import stats
from enum import Enum


logging.basicConfig(level=logging.INFO, format='%(asctime)s | %(levelname)s | %(message)s')
logger = logging.getLogger(__name__)


class ChannelSize(Enum):
    XL = 1
    L = 2
    S = 3
    XS = 4


class ChannelType(Enum):
    LINE = 1
    CURVE = 2


class MeasurementLoc(Enum):
    # Values of this enum are always of type string.
    LINE1 = '1'
    CURVE1 = '2'
    LINE2 = '3'
    CURVE2 = '4'


data_dir = '/home/mkrause/data/clearance'
datafile = 'widths_data.json'
figname = 'plot.png'
labels_and_data = 'labels.json'

ALPHA = 0.05  # constant for stats


def get_data() -> dict:
    with open(os.path.join(data_dir, datafile)) as json_file:
        data = json.load(json_file)

    return data


def get_data_for_specific_channel(data: dict, size: str, measure_loc: str) -> list:
    res = []
    for dct in data[0][size]:
        for key, val in dct.items():
            if key == measure_loc:
                res.append(val)
    
    return res


def is_equal_vars(sample1: list, sample2: list, alpha: float) -> bool:
    """Use Levene's test"""
    vars = stats.levene(sample1, sample2)
    if vars.pvalue < alpha:
        return False
    
    return True


def is_samples_not_different(sample1: list, sample2: list, alpha: float) -> bool:
    """Use Student's t-test"""
    if is_equal_vars(sample1, sample2, alpha):
        test_res = stats.ttest_ind(sample1, sample2)
        if test_res.pvalue < alpha:
            logger.warning("Values are different")
            return False # sample are different
        
        logger.info("Values are not different")
        
        return True


def combine_like_samples(data: dict, channel_size: str, channel_type: str) -> list:
    """Return list of combined measurement in two measurement locations if samples are not different"""
    widths = []
    if channel_type == ChannelType.LINE.name:
        widths_1 = get_data_for_specific_channel(data=data, size=channel_size, measure_loc=MeasurementLoc.LINE1.value)
        widths_2 = get_data_for_specific_channel(data=data, size=channel_size, measure_loc=MeasurementLoc.LINE2.value)
    elif channel_type == ChannelType.CURVE.name:
        widths_1 = get_data_for_specific_channel(data=data, size=channel_size, measure_loc=MeasurementLoc.CURVE1.value)
        widths_2 = get_data_for_specific_channel(data=data, size=channel_size, measure_loc=MeasurementLoc.CURVE2.value)
    
    if is_samples_not_different(sample1=widths_1, sample2=widths_2, alpha=ALPHA):
        widths = widths_1 + widths_2

    return widths


def main():
    data = get_data()

    # XL:
    widths_XL_line = combine_like_samples(data=data, channel_size=ChannelSize.XL.name, channel_type=ChannelType.LINE.name)
    widths_XL_curve = combine_like_samples(data=data, channel_size=ChannelSize.XL.name, channel_type=ChannelType.CURVE.name)
    
    print(f'widths_XL_line: {widths_XL_line}')
    print(f'widths_XL_curve: {widths_XL_curve}')



if __name__ == '__main__':
    main()
