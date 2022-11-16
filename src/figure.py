#!/usr/bin/env python3

import os
import logging
import pandas as pd
import matplotlib.pyplot as plt
from src.config import Config


class Figure:

    @classmethod
    def figure_handle(cls) -> tuple:
        fig, ax = plt.subplots()
        ax.set_xlim(Config.xlims['min'], Config.xlims['max'])
        ax.set_box_aspect(1)
        ax.legend(Config.legend)
        return fig, ax

    @classmethod
    def plot(cls, excel_filename, ax, sheet_name='Sheet1', symbol='-ob', legend=False):
        df = pd.read_excel(excel_filename, sheet_name=sheet_name, index_col=1)
        pd.DataFrame.info(df)
        plt.gca()
        xvals = df.index
        yvals = df['y']
        yerr = df['err']
        plt.yscale('log')
        plt.errorbar(
            xvals, yvals,
            yerr=yerr,
            fmt=symbol,
            capsize=4
        )
        plt.xlabel(Config.plot_xlabel)
        plt.ylabel(Config.plot_ylabel)
        ax.set_xlim(Config.xlims['min'], Config.xlims['max'])
        ax.set_box_aspect(1)
        if legend:
            ax.legend(Config.legend, loc=Config.legend_loc)

    @classmethod
    def save(cls, excel_filename, dest):
        figure_filename = excel_filename.split('.')[0] + '.png'
        dest = os.path.join(dest, figure_filename)
        plt.savefig(dest)
        if os.path.exists(f'{dest}'):
            logging.info(f'Wrote file {figure_filename} to {dest}')
        else:
            logging.warning('Could not write file')
