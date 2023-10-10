#!/usr/bin/env python3

import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import os
import numpy as np
from statistics import mean, stdev
from typing import Tuple


class PlotUtils:

    glob_figpath = None
    user_fig_directory = '/data'

    @classmethod
    def set_user_figure_dir(cls, user_fig_directory: str = None):
        user_home_dir = os.path.expanduser('~')
        if user_fig_directory is None:
            user_fig_directory = cls.user_fig_directory
        cls.glob_figpath = os.path.join(user_home_dir, user_fig_directory)
        if not os.path.exists(cls.glob_figpath):
            os.makedirs(cls.glob_figpath)

    @classmethod
    def plot_scatter(cls, xdata: list, ydata: list, yerr: list, title=None, xlabel=None, xlabel_prefix=None, xlim=None,
                     xticklabels: str = None, ylabel=None, figname=None, ylim=None, yscale='linear',
                     xticks: list = None, plotsize_adjust: dict = None, hide_inner: bool = False, capsize=5,
                     subplot_config: dict = {'nrows': 1, 'ncols': 2}, colors=None, errbar_dir: str = 'both') -> None:
        """Create scatterplot of data with standard deviation as errorbars"""
        fig, ax = plt.subplots(subplot_config['nrows'], subplot_config['ncols'])
        fig.suptitle(title)
        # TODO: what's the deal with the commented out code?
        # if not colors:
        #     colors = ['tab:blue', 'tab:orange', 'tab:green']
        if errbar_dir == 'up':
            if len(yerr) == 1:
                _yerr = np.zeros((2, len(yerr[0])))
                _yerr[1, :] = yerr[0]
                yerr[0] = _yerr
            else:
                for idx, err in enumerate(yerr):
                    _yerr = np.zeros((2, len(err)))
                    _yerr[1, :] = err
                    yerr[idx] = _yerr
        data = list(zip(xdata, ydata, yerr))
        if subplot_config['nrows'] == 1 and subplot_config['ncols'] == 1:
            for idx, datum in enumerate(data):
                if colors is not None:
                    ax.errorbar(datum[0], datum[1], yerr=datum[2], capsize=capsize,
                                ecolor=mcolors.TABLEAU_COLORS[colors[idx]],
                                marker='o', markerfacecolor=mcolors.TABLEAU_COLORS[colors[idx]],
                                markeredgecolor=mcolors.TABLEAU_COLORS[colors[idx]], markersize=10, linestyle='none')
                else:
                    color = 'black'
                    ax.errorbar(datum[0], datum[1], yerr=datum[2], capsize=capsize,
                                ecolor=color, markerfacecolor=color, markeredgecolor=color,
                                marker='o', markersize=10, linestyle='none')
            ax.set_xlabel(xlabel)
            ax.set_ylabel(ylabel)
            ax.set_yscale(yscale)
            if xticks:
                ax.set_xticks(xticks)
            if xlim:
                ax.set_xlim(xlim)
            if ylim:
                ax.set_ylim(ylim)
            cls.__force_aspect(ax=ax)
        else:
            for idx, datum in enumerate(data):
                if colors:
                    ax[idx].errorbar(datum[0], datum[1], yerr=datum[2], capsize=capsize,
                                     ecolor=mcolors.TABLEAU_COLORS[colors[idx]],
                                     marker='o', markerfacecolor=mcolors.TABLEAU_COLORS[colors[idx]],
                                     markeredgecolor=mcolors.TABLEAU_COLORS[colors[idx]],
                                     markersize=10, linestyle='none')
                else:
                    ax[idx].errorbar(datum[0], datum[1], yerr=datum[2], capsize=capsize,
                                     marker='o',  markersize=10, linestyle='none')
                if xlabel_prefix:
                    ax[idx].set_xlabel(f'{xlabel_prefix} ({xlabel[idx]})')
                else:
                    ax[idx].set_xlabel(f'{xlabel[idx]}')
                ax[idx].set_xticks(datum[0])
                ax[idx].set_ylabel(ylabel)
                if xlim:
                    ax[idx].set_xlim(
                        xlim)  # x-ticks are too far apart and to close to the edge of the frame - this corrects for that
                ax[idx].set_yscale(yscale)
                if ylim:
                    ax[idx].set_ylim(ylim)
            # Hide x labels and tick labels for top plots and y ticks for right plots.
        if hide_inner:
            for a in ax.flat:
                a.label_outer()
        else:
            fig.tight_layout(pad=4.0)
        if plotsize_adjust:
            fig.subplots_adjust(left=plotsize_adjust['left'],
                                right=plotsize_adjust['right'],
                                top=plotsize_adjust['top'],
                                bottom=plotsize_adjust['bottom'])
        # if xticklabels:
        #        ax.set_xticklabels(xticklabels)
        if figname:
            figpath = os.path.join(cls.glob_figpath, figname)
            fig.savefig(figpath)

    @staticmethod
    def __force_aspect(ax: plt.Axes, aspect: int = 1) -> None:
        """Sets aspect ratio of plot
        --aspect: positive integer denoting the denominator to compute the aspect ratio
        """
        # TODO: seems to work only for images, but not, e.g.,. for scatter plots
        im: list = ax.get_images()
        if im:
            extent = im[0].get_extent()
            ax.set_aspect(abs((extent[1] - extent[0]) / (extent[3] - extent[2])) / aspect)

    @staticmethod
    def lst_tuples_to_lists(data: list) -> tuple[list, list]:
        """Return two lists
        @param data:    list of one or more 2-tuples.
        @return:        two lists, the first list contains all items at index 0 of each
                        2-tuple, the other each items at index 1
        """
        idx_ydata = 0
        idx_yerr = 1
        return list(map(lambda x: x[idx_ydata], data)), list(map(lambda x: x[idx_yerr], data))

