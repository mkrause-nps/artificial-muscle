#!/usr/bin/env python3

import os
import numpy as np
import matplotlib.pyplot as plt
import csv
import json
import logging

data_dir = '/home/mkrause/data/clearance'
datafile = 'summary.csv'
figname = 'plot.png'
labels_and_data = 'labels.json'

# Get labels and data structures:
with open(os.path.join(data_dir, labels_and_data)) as json_file:
    data_dct = json.load(json_file)


def read_datafile() -> list:
    """A dum reader"""
    data = []
    with open(os.path.join(data_dir, datafile), 'r') as fp:
        reader = csv.reader(fp)
        for line in reader:
            data.append(line)

    return data
    

def reformat_data(data: list) -> dict:
    """Return data in a format suitable for plotting"""
    for idx, datum in enumerate(data):
        if idx == 0:
            data_dct['labels']['values'] = data[idx][1:]
        elif idx == 1:
            data_dct['means'] = [float(el) for el in data[idx][1:]]
        elif idx == 2:
            data_dct['stdev'] = [float(el) for el in data[idx][1:]]
        else:
            raise IndexError("index is out of range - only 3 entries expected")

    return data_dct


def create_plot(data: dict) -> None:
    x = data['labels']['values']
    y = data['means']
    yerr = data['stdev']

    print(f'x: {x}')
    print(f'y: {y}')
    print(f'err: {yerr}')

    # plot:
    fig, ax = plt.subplots()

    ax.errorbar(x, y, yerr, fmt='o', linewidth=2, capsize=6)

    ax.set(
        xlim=(0, 4), xticks=np.arange(-1, 4),
        ylim=(-10, 120)
    )

    ax.set_title(data['labels']['title'])
    ax.set_xlabel(data['labels']['xlabel'])
    ax.set_ylabel(data['labels']['ylabel'])

    fig.tight_layout()

    #plt.show()
    logging.info(f'Saving plot as {figname}')
    plt.savefig(os.path.join(data_dir, figname))


def main():
    _data = read_datafile()
    data = reformat_data(_data)
    create_plot(data)


if __name__ == '__main__':
    main()
