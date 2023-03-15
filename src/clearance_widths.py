#!/usr/bin/env python3

import os
import numpy as np
import matplotlib.pyplot as plt
import csv
import json
import logging
from scipy import stats

data_dir = '/home/mkrause/data/clearance'
datafile = 'widths_data.json'
figname = 'plot.png'
labels_and_data = 'labels.json'

alpha = 0.05

logging

def get_data() -> dict:
    with open(os.path.join(data_dir, datafile)) as json_file:
        data = json.load(json_file)

    return data

def get_data_for_specific_channel(data: dict, size: str, channel: str) -> list:
    res = []
    for dct in data[0][size]:
        for key, val in dct.items():
            if key == channel:
                res.append(val)
    
    return res


def is_equal_vars(sample1: list, sample2: list, alpha: float) -> bool:
    """Use Levene's test"""
    vars = stats.levene(sample1, sample2)
    if vars.pvalue < alpha:
        return False
    
    return True


def is_samples_not_different(sample1: list, sample2: list) -> bool:
    """Use Student's t-test"""
    if is_equal_vars(sample1, sample2, alpha):
        test_res = stats.ttest_ind(sample1, sample2)
        if test_res.pvalue < alpha:
            return False # sample are different
        
        return True


def main():
    data = get_data()
    xl_1 = get_data_for_specific_channel(data=data, size='XL', channel='1')
    xl_3 = get_data_for_specific_channel(data=data, size='XL', channel='3')
    if is_samples_not_different(sample1=xl_1, sample2=xl_3, alpha):
        xl_serpentine_line = xl_1 + xl_3
    
    #print(channel_widths)



if __name__ == '__main__':
    main()
