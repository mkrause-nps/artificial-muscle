#!/usr/bin/env python3

"""
Configuration file

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
    output_dir = 'C:\\Users\\mkrause.RIZIA-PC\\OneDrive - Naval Postgraduate School\\artificial_muscle\\data'
    plot_xlabel = 'fraction CNF added (weight %)'
    plot_ylabel = 'conductivity (S/m)'
    xlims = {'min': 0, 'max': 12}
    legend = ['unfiltered', 'filtered']
    legend_loc = 'lower right'
