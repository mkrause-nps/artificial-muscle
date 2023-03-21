#!/usr/bin/env python3

"""
Configuration file

If you work on WSL2 Linux it seems best to transfer any data files to the Linux instance
and set the output_dir accordingly. I've made a few attempts to call files from Linux on
Windows 10, but all failed.

Parameters
----------
output_dir: string
             Directory the Excel files reside and the figure files should be
             written to on the system.
plot_xlabel: str
plot_ylabel: str
             The axis labels of the plot.
xlims: dict
       The minimum and maximum value of the x-axis of the plot.
legend: list
        Strings to describe the data plotted.
legend_loc: str
            A Matplotlib formatting string that determines the position of the
            legend on the plot.
"""


class Config:
    #output_dir: str = 'C:\\Users\\mkrause.RIZIA-PC\\OneDrive - Naval Postgraduate School\\artificial_muscle\\data'
    output_dir: str = '/home/mkrause/data/width/'
    #output_dir: str = '/home/mkrause/data/conductivity/'
    suffix: str = None,
    plot_title: str = None,
    plot_xlabel: str = 'fraction CNF added (weight %)'
    plot_ylabel: str = 'conductivity (S/m)'
    xlims: dict = {'min': 0, 'max': 14}
    ylims: dict = None  # {'min': 10e-8, 'max': 10e2}
    legend: list = []  # ['unfiltered', 'filtered']
    legend_loc: str = 'upper left'  # 'lower right'
    measured_widths_col_name: str = 'widths_um'
    py_all: str = 'py_all'
