#!/usr/bin/env python3

import os
import logging
import sys

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
    def get_dataframe(cls, excel_filename):
        if Config.py_all == '' or Config.py_all.isspace():
            raise ValueError()

        return pd.read_excel(excel_filename, sheet_name=Config.py_all)

    @classmethod
    def plot(cls, excel_filename, ax,
             sheet_name='Sheet1', symbol='-ob', plot_type='linear', title=None, legend=False, diagonal=False):
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
        if plot_type == 'linear':
            ax.set_ylim(Config.xlims['min'], Config.xlims['max'])
        ax.set_box_aspect(1)
        if legend:
            ax.legend(Config.legend, loc=Config.legend_loc)

    @classmethod
    def save(cls, excel_filename, dest, suffix: str):
        figure_filename = excel_filename.split('.')[0] + '_' + suffix + '.png'
        dest = os.path.join(dest, figure_filename)
        plt.savefig(dest)
        if os.path.exists(f'{dest}'):
            logging.info(f'Wrote file {figure_filename} to {dest}')
        else:
            logging.warning('Could not write file')

    @staticmethod
    def __plot_diagonal():
        xvals = range(0, Config.xlims['max'])
        yvals = range(0, Config.xlims['max'])
        plt.plot(xvals, yvals, '--k', label='_nolegend_')
