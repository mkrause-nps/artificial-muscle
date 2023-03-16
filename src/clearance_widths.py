#!/usr/bin/env python3

import os
import numpy as np
import matplotlib.pyplot as plt
import csv
import json
import logging
import statistics
from scipy import stats
from enum import Enum
from typing import Tuple


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
labels = (ChannelSize.XL.name, ChannelSize.L.name, ChannelSize.S.name)

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


def get_mean_and_stdev(data: list) -> Tuple[float, float]:
    """Compute mean and standard deviation from sample"""
    mean = statistics.mean(data)
    stdev = statistics.stdev(data)

    return mean, stdev

def get_means_and_stdevs(xl: list, l: list, s: list) -> Tuple[list, list]:
    means = []
    stdevs = []

    xl_mean, xl_stdev = get_mean_and_stdev(xl)
    means.append(xl_mean)
    stdevs.append(xl_stdev)

    l_mean, l_stdev = get_mean_and_stdev(l)
    means.append(l_mean)
    stdevs.append(l_stdev)

    s_mean, s_stdev = get_mean_and_stdev(s)
    means.append(s_mean)
    stdevs.append(s_stdev)

    return means, stdevs


def create_plot_line_measurement(xl: list, l: list, s: list) -> None:
    title = 'Line Portion of Serpentine Channels'
    xlabel = 'Relative Channel Size'
    ylabel = 'Channel Widths (um)'
    figname = 'channel_widths_line_portion'
    means, stdevs = get_means_and_stdevs(xl=xl, l=l, s=s)
    ymax = 800
    create_plot(x=labels, y=means, yerr=stdevs, title=title, xlabel=xlabel, ylabel=ylabel, figname=figname, ymax=ymax)


def create_plot_curve_measurement(xl: list, l: list, s: list) -> None:
    title = 'Curve Portion of Serpentine Channels'
    xlabel = 'Relative Channel Size'
    ylabel = 'Channel Widths (um)'
    figname = 'channel_widths_curve_portion'
    means, stdevs = get_means_and_stdevs(xl=xl, l=l, s=s)
    ymax = 1200
    create_plot(x=labels, y=means, yerr=stdevs, title=title, xlabel=xlabel, ylabel=ylabel, figname=figname, ymax=ymax)


def create_plot(x: list, y: list, yerr: list, title: str, xlabel: str, ylabel: str, figname: str, ymax: int) -> None:
    # plot:
    fig, ax = plt.subplots()

    ax.errorbar(x, y, yerr, fmt='o', linewidth=2, capsize=6)

    ax.set(
        xlim=(0, 3), xticks=np.arange(-1, 3),
        ylim=(0, ymax)
    )

    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)

    fig.tight_layout()

    #plt.show()
    logging.info(f'Saving plot as {figname}')
    plt.savefig(os.path.join(data_dir, figname))


def write_summary_results_to_file(xl: list, l: list, s: list, res_type: str) -> None:
    means, stdevs = get_means_and_stdevs(xl=xl, l=l, s=s)
    filename = 'channels_widths_summary_' + res_type + '.csv'
    filepath = os.path.join(data_dir, filename)
    num_significant_digits = 1
    with open(filepath, 'w', newline='') as csvfile:
        fieldnames = ['summary', ChannelSize.XL.name, ChannelSize.L.name, ChannelSize.S.name]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        writer.writerow({'summary': 'means:', ChannelSize.XL.name: round(means[0], num_significant_digits), ChannelSize.L.name: round(means[1], num_significant_digits), ChannelSize.S.name: round(means[2], num_significant_digits)})
        writer.writerow({'summary': 'standard deviations:', ChannelSize.XL.name: round(stdevs[0], num_significant_digits), ChannelSize.L.name: round(stdevs[1], num_significant_digits), ChannelSize.S.name: round(stdevs[2], num_significant_digits)})
        writer.writerow({'summary': 'All values are um',  ChannelSize.XL.name: '', ChannelSize.L.name: '', ChannelSize.S.name: ''})


def main():
    # Get data from file:
    data = get_data()

    # Collect values for each channel size and channel type (i.e., measurement location) and combine them into one list:

    # LINE measurement loc:
    # XL:
    widths_XL_line = combine_like_samples(data=data, channel_size=ChannelSize.XL.name, channel_type=ChannelType.LINE.name)
    print(f'widths_XL_line: {widths_XL_line}')

    # L:
    widths_L_line = combine_like_samples(data=data, channel_size=ChannelSize.L.name, channel_type=ChannelType.LINE.name)    
    print(f'widths_L_line: {widths_L_line}')

    # S:
    widths_S_line = combine_like_samples(data=data, channel_size=ChannelSize.S.name, channel_type=ChannelType.LINE.name)   
    print(f'widths_S_line: {widths_S_line}')

    create_plot_line_measurement(xl=widths_XL_line, l=widths_L_line, s=widths_S_line)
    write_summary_results_to_file(xl=widths_XL_line, l=widths_L_line, s=widths_S_line, res_type=ChannelType.LINE.name)


    # CURVE measurement loc:
    widths_XL_curve = combine_like_samples(data=data, channel_size=ChannelSize.XL.name, channel_type=ChannelType.CURVE.name)
    print(f'widths_XL_curve: {widths_XL_curve}')

    widths_L_curve = combine_like_samples(data=data, channel_size=ChannelSize.L.name, channel_type=ChannelType.CURVE.name)
    print(f'widths_L_curve: {widths_L_curve}')

    widths_S_curve = combine_like_samples(data=data, channel_size=ChannelSize.S.name, channel_type=ChannelType.CURVE.name)
    print(f'widths_S_curve: {widths_S_curve}')

    create_plot_curve_measurement(xl=widths_XL_curve, l=widths_L_curve, s=widths_S_curve)
    write_summary_results_to_file(xl=widths_XL_curve, l=widths_L_curve, s=widths_S_curve, res_type=ChannelType.CURVE.name)

if __name__ == '__main__':
    main()
