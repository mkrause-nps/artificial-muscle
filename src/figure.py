#!/usr/bin/env python3

import os
import logging
import numpy
import pandas as pd
import matplotlib.axes
import matplotlib.pyplot as plt
from src.config import Config


class Figure:

    @classmethod
    def get_figure_handle(cls) -> tuple:
        global ax
        fig, ax = plt.subplots()
        ax.set_xlim(Config.xlims['min'], Config.xlims['max'])
        ax.set_box_aspect(1)
        ax.legend(Config.legend)
        return fig, ax

    @classmethod
    def get_dataframe(cls, excel_filename) -> pd.DataFrame:
        """Load data in tab 'py_all' into Pandas DF, from the main Excel spreadsheet file."""
        if Config.py_all == '' or Config.py_all.isspace():
            raise ValueError()

        return pd.read_excel(excel_filename, sheet_name=Config.py_all)

    @classmethod
    def plot_conductivity(cls, excel_filename, sheet_name='Sheet1', symbol='-ob', y_scale='linear',
                          ax_obj: matplotlib.axes = None, title=None, legend=False, diagonal=False) -> matplotlib.axes:
        """Creates scatter plot and returns its axes object"""
        df = pd.read_excel(excel_filename, sheet_name=sheet_name, index_col=1)
        # pd.DataFrame.info(df)
        # plt.gca()
        if not ax_obj:
            _, ax_obj = cls.get_figure_handle()
        xvals = df.index
        yvals = df['y']
        yerr = df['err']
        ax_obj.set_yscale(y_scale)
        ax_obj.errorbar(
            xvals, yvals,
            yerr=yerr,
            fmt=symbol,
            capsize=4
        )
        if diagonal:
            cls.__plot_diagonal()
        ax_obj.set_xlabel(Config.plot_xlabel)
        ax_obj.set_ylabel(Config.plot_ylabel)
        ax_obj.set_title(title)
        ax_obj.set_xlim(Config.xlims['min'], Config.xlims['max'])
        if Config.ylims:
            ax_obj.set_ylim(Config.ylims['min'], Config.ylims['max'])
        if y_scale == 'linear':
            ax_obj.set_ylim(Config.xlims['min'], Config.xlims['max'])
        ax_obj.set_box_aspect(1)
        if legend:
            ax_obj.legend(Config.legend, loc=Config.legend_loc)
        else:
            ax_obj.legend('', frameon=False)  # otherwise that leaves an ugly small gray frame in the upper right corner

        return ax_obj

    @classmethod
    def plot_differences(cls, x: numpy.ndarray, y: numpy.ndarray, material: str, direction: str):
        """Stem plot"""
        title = f'Channel widths of {material}, printed {direction}'
        xlabel = 'channel ID'
        ylabel = rf'after width - before width ($\mu$m)'

        # Create plot.
        fig, ax_obj = plt.subplots()
        ax_obj.stem(x, y)
        ax_obj.set_title(title)
        ax_obj.set(xlabel=xlabel, ylabel=ylabel)

    @classmethod
    def plot_relative_error(cls, widths: pd.DataFrame, diffs: pd.DataFrame, material: str, direction: str) -> None:
        title = f'{material}, print orientation {direction}'
        xlabel = 'Set width ($\mu m$)'
        ylabel = 'Relative error of measured width (%)'
        pass

    @classmethod
    def plot_widths_fractional_differences(cls, x: numpy.ndarray, y: numpy.ndarray, yerr: numpy.ndarray, material: str,
                                           direction: str):
        """Scatter plot with errors"""
        title = f"{material.replace('_', ' ')}, printed {direction}"
        xlabel = 'Channel ID'
        ylabel = rf'Fractional expansion (%)'
        color = 'gray'

        # Create plot.
        fig, ax_obj = plt.subplots()
        plt.errorbar(x=x, y=y, yerr=yerr, color=color, fmt='o', capsize=8)
        ax_obj.set_title(title)
        ax_obj.set(xlabel=xlabel, ylabel=ylabel)
        ax_obj.set_ylim(-10, 70)
        cls.__plot_zero_x_line()

    @classmethod
    def plot_channel_widths_and_differences(cls, widths: pd.DataFrame, diffs: pd.DataFrame, material: str,
                                            direction: str, unity_line: bool = False):
        """Scatter plot of width prior to and past baking and their differences in one graph"""
        title = f'Channel widths of {material.replace("_", " ")}, printed {direction}'
        xlabel = 'Set channel width ($\mu$m)'
        ylabel = rf'Measured channel width ($\mu$m)'
        ylabel2 = rf'after width - before width ($\mu$m)'

        fig, ax1 = plt.subplots()

        # Create plot.
        plt.errorbar(x=widths['channel_id'], y=widths['width_prior'], yerr=widths['width_prior_err'],
                     fmt='-ob', capsize=4)
        plt.errorbar(x=widths['channel_id'], y=widths['width_past'], yerr=widths['width_past_err'],
                     fmt='-or', capsize=4)

        # Compose axis and labels for right y-axis:
        ax1.set_title(title)
        ax1.set(xlabel=xlabel, ylabel=ylabel)
        ax1.set_xlim(Config.xlims['min'], Config.xlims['max'])
        ax1.set_ylim(Config.ylims['min'], Config.ylims['max'])
        if material == 'black_resin' and direction == 'perpendicular':
            ax1.legend(Config.legend, loc='lower right')
        else:
            ax1.legend(Config.legend, loc=Config.legend_loc)
        ax1.set_box_aspect(1)

        if unity_line:
            cls.__plot_diagonal()

        # Compose axis and labels for left y-axis:
        ax2 = ax1.twinx()  # instantiate a second axis that shares the same x-axis
        color = 'green'
        plt.scatter(widths['channel_id'], diffs['width_diff'], color=color)
        if direction == 'parallel':
            ax2.set_ylim(0, 300)
        elif material == 'black_resin' and direction == 'perpendicular':
            ax2.set_ylim(0, 400)
        else:
            ax2.set_ylim(0, 400)
        ax2.set_ylabel(ylabel2, color=color)  # we already handled the x-label with ax1
        ax2.tick_params(axis='y', labelcolor=color)
        ax2.set_box_aspect(1)

    @classmethod
    def save(cls, excel_filename: str, dest: str, suffix: str) -> None:
        """Write file with plot to disk in PNG and SVG format"""
        cls.__save_figure_as(filename=excel_filename, dest=dest, suffix=suffix, _format='.png')
        cls.__save_figure_as(filename=excel_filename, dest=dest, suffix=suffix, _format='.svg')

    @classmethod
    def __save_figure_as(cls, filename: str, dest: str, suffix: str, _format: str) -> None:
        figure_filename = cls.__get_filename(filename) + '_' + suffix + _format
        dest = os.path.join(dest, figure_filename)
        plt.savefig(dest)
        if os.path.exists(f'{dest}'):
            logging.info(f'Wrote file {figure_filename} to {dest}')
        else:
            logging.warning('Could not write file')

    @staticmethod
    def __plot_diagonal() -> None:
        """Add a diagonal line to the plot (useful if x- and y-axis have same units and scale)."""
        xvals = range(0, Config.xlims['max'])
        yvals = range(0, Config.xlims['max'])
        plt.plot(xvals, yvals, '--k', label='_nolegend_')

    @staticmethod
    def __plot_zero_x_line() -> None:
        """Add a line parallel to the x-axis."""
        plt.axhline(y=0, color='k', linestyle='--')

    @staticmethod
    def __get_filename(filename: str) -> str:
        """Getting the filename depending on whether it is absolute or relative."""
        num_dots = filename.count('.')
        if num_dots == 1:
            return filename.split('.')[0]
        else:
            return filename.split('.')[-2].split('\\')[-1]
