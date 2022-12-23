#!/usr/bin/env python3

import os
import logging
import sys

import numpy
import pandas as pd
import matplotlib.pyplot as plt
from src.config import Config


class Figure:

    @classmethod
    def get_figure_handle(cls) -> tuple:
        fig, ax = plt.subplots()
        ax.set_xlim(Config.xlims['min'], Config.xlims['max'])
        ax.set_box_aspect(1)
        ax.legend(Config.legend)
        return fig, ax

    @classmethod
    def get_dataframe(cls, excel_filename) -> pd.DataFrame:
        if Config.py_all == '' or Config.py_all.isspace():
            raise ValueError()

        return pd.read_excel(excel_filename, sheet_name=Config.py_all)

    @classmethod
    def plot(cls, excel_filename, ax,
             sheet_name='Sheet1', symbol='-ob', plot_type='linear', title=None, legend=False, diagonal=False) -> None:
        df = pd.read_excel(excel_filename, sheet_name=sheet_name, index_col=1)
        pd.DataFrame.info(df)
        plt.gca()
        if diagonal:
            cls.__plot_diagonal()
        xvals = df.index
        yvals = df['y']
        yerr = df['err']
        plt.yscale(plot_type)
        plt.errorbar(
            xvals, yvals,
            yerr=yerr,
            fmt=symbol,
            capsize=4
        )
        plt.xlabel(Config.plot_xlabel)
        plt.ylabel(Config.plot_ylabel)
        plt.title(title)
        ax.set_xlim(Config.xlims['min'], Config.xlims['max'])
        if Config.ylims:
            ax.set_ylim(Config.ylims['min'], Config.ylims['max'])
        if plot_type == 'linear':
            ax.set_ylim(Config.xlims['min'], Config.xlims['max'])
        ax.set_box_aspect(1)
        if legend:
            ax.legend(Config.legend, loc=Config.legend_loc)

    @classmethod
    def plot_differences(cls, x: numpy.ndarray, y: numpy.ndarray, material: str, direction: str, past: str, prior: str):
        title = f'Channel widths of {material}, printed {direction}'
        xlabel = 'channel ID'
        ylabel = rf'{past} width - {prior} width ($\mu$m)'

        # Create plot.
        fig, ax = plt.subplots()
        ax.stem(x, y)
        ax.set_title(title)
        ax.set(xlabel=xlabel, ylabel=ylabel)

    @classmethod
    def save(cls, excel_filename: str, dest: str, suffix: str) -> None:
        figure_filename = cls.__get_filename(excel_filename) + '_' + suffix + '.png'
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
    def __get_filename(filename: str):
        """Getting the filename depending on whether it is absolute or relative."""
        num_dots = filename.count('.')
        if num_dots == 1:
            return filename.split('.')[0]
        else:
            return  filename.split('.')[-2].split('\\')[-1]
