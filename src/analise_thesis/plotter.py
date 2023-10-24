#!/usr/bin/env python3
from pprint import pprint
from src.analise_thesis.channel_data import ChannelData
from src.analise_thesis.restructure import Restructure
from src.analise_thesis.weighted_average import WeightedAverage
from src.plot_utils import PlotUtils


class MyList(list):
    """Extends list class with a method that pads a list with specific values"""

    def ljust(self, n: int, fill_value: str | int | None = ''):
        """Pad list in place with fill_value, with total length n"""
        return self + [fill_value] * (n - len(self))


class Plotter:
    def __init__(self, data: list[tuple], nrows: int, ncols: int, xlabel: str, ylabel: str, xlim: list, ylim: list,
                 aspect: int, capsize: int, fig_format: str, is_title_and_labels: bool = True,
                 fontsize: float = 12.0) -> None:
        """

        @param data:    a list of one or more three-tuples, which represents data of one channel width on one chip of a
                        specific type, e.g., (896, 1, 'hard')
        @param nrows:   refers to the rows and columns of a figure, respectively
        @param ncols:
        @param xlabel:  figure x- and y- labels
        @param ylabel:
        @param xlim:    figure x- and y-limits
        @param ylim:
        @type aspect:   (float) set the aspect ratio of x- and y-axis, regardless of data ranges
        @param capsize: the length of the horizontal line on top and bottom of an error bar
        @type fig_format: (str) 'png' or 'svg' for vector graphics
        @type is_title_and_labels: (bool) figure has title and x- and y-labels if true
        @param fontsize: font size for ticks on x- and y-axes in points
        """

        self.is_title_and_labels = is_title_and_labels
        self.data: list[tuple] = data
        self.SAMPLE_NUM_CUTOFF = 1
        self.nrows = nrows
        self.ncols = ncols
        self.xlabel = xlabel
        self.ylabel = ylabel
        self.xlim = xlim
        self.ylim = ylim
        self.aspect = aspect
        self.capsize = capsize
        self.fig_format = fig_format
        self.fontsize = fontsize
        self.is_title_and_labels = is_title_and_labels

    def run_individual_chips(self) -> None:
        lxlim = 0
        rxlim = 6
        """Plot all injections of a single chip ID and write plot to disk"""
        if self.data:
            for datum in self.data:
                channel_data = ChannelData(channel_width=datum[0], chip_id=datum[1], chip_type=datum[2])
                xdata, ydata, yerr = channel_data.get_data()
                xdata = list(range(1, rxlim))  # HACK: override xdata so x-axis of all plots has same number of elements
                xticks = list(range(1, len(xdata) + 1))  # list(range(1, channel_data.num_injections + 1))
                title = f'Chip type: {datum[2]}, id: {datum[1]}, width: {datum[0]}'
                figname = f'chip_id_{datum[1]}_type_{datum[2]}_width_{datum[0]}.{self.fig_format}'
                if self.is_title_and_labels:
                    PlotUtils.plot_scatter(
                        xdata, ydata, yerr=yerr, nrows=self.nrows, ncols=self.ncols, title=title,
                        xlabel=self.xlabel, ylabel=self.ylabel, xlim=[lxlim, rxlim], xticks=xticks,
                        fontsize=self.fontsize, figname=figname, fig_format=self.fig_format,
                        aspect=self.aspect, capsize=self.capsize, colors=None)
                else:
                    PlotUtils.plot_scatter(
                        xdata, ydata, yerr=yerr, nrows=self.nrows, ncols=self.ncols, xlim=[lxlim, rxlim],
                        xticks=xticks, fontsize=self.fontsize, figname=figname,
                        fig_format=self.fig_format, aspect=self.aspect, capsize=self.capsize,
                        colors=None)

    def get_averaged_channel_data(self, data_subset: list[tuple]) -> dict | None:
        """Return weighted average and standard deviation for one channel width from all chips
        @param data_subset: a list of tuples, where each tuple has the same channel width
        @return: dictionary with x-data, and weighted averages of y-data and the standard deviation,
                 and other important information
        """
        out_data: dict = {}
        chip_width = data_subset[0][0]
        out_data['chip_width'] = chip_width
        chip_type = data_subset[0][2]
        out_data['chip_type'] = chip_type
        out_data['number_of_chips'] = len(data_subset)

        if self.is_channel_triaged(data_subset):
            print(f'width {chip_width} has less than {self.SAMPLE_NUM_CUTOFF} samples - triaged')
            return None
        channel_data: list = []
        for id_ in data_subset:
            print(f'processing chip ID: {id_[1]}')
            channel_data.append(ChannelData(channel_width=id_[0], chip_id=id_[1], chip_type=id_[2]))

        # Aggregate data:
        xdata, ydata_yerr_agg = self.aggregate_from_one_channel(channel_data)

        # Restructure data:
        restructured_data = Restructure.restructure(tuple(ydata_yerr_agg))
        if not restructured_data:
            return None
        print(f'data type of restructured_data: {str(type(restructured_data))}')
        for item in restructured_data:
            pprint(f'item: {item}')
        tups: list = []
        for data in restructured_data:
            weighted_ydata_, weighted_yerr_ = WeightedAverage.get(data)
            tups.append((weighted_ydata_, weighted_yerr_))
            print(f'weighted_ydata_: {weighted_ydata_}, weighted_yerr_: {weighted_yerr_}')
        weighted_ydata, weighted_yerr = PlotUtils.lst_tuples_to_lists(data=tups)

        # assert(len(xdata) == len(list(range(1, len(ydata_yerr_agg) + 1))))  # FAILS!

        max_number_injections = max([ch.num_injections for ch in channel_data])

        out_data['x_data'] = xdata  # list(range(1, max_number_injections))
        print(f'xdata: {xdata}; max_number_injections: {max_number_injections}')
        out_data['number_of_injections'] = max_number_injections
        out_data['y_data'] = weighted_ydata
        out_data['y_err'] = weighted_yerr

        title = f'Weighted average: Chip type: {chip_type}, width: {chip_width}'
        figname = f'width_{chip_width}_type_{chip_type}_weighted_data.{self.fig_format}'
        print(f'printing: {figname}')

        # Ticks on the x-axis are the chip widths we measured from:
        xticks = list(range(1, len(xdata) + 1))

        PlotUtils.plot_scatter(xdata, weighted_ydata, yerr=weighted_yerr, nrows=self.nrows, ncols=self.ncols,
                               title=title, xlabel=self.xlabel, ylabel=self.ylabel, xticks=xticks, figname=figname,
                               fig_format=self.fig_format, capsize=self.capsize, colors=None)

        return out_data

    def get_channel_list(self) -> list:
        """Return a set (but cast as a list) of channel widths from data"""
        channels = list(set(tup[0] for tup in self.data))
        return sorted(channels)

    def is_channel_triaged(self, channel_list: list[tuple]) -> bool:
        """Return true of the number of samples for a given channel width is less than 2"""
        return len(channel_list) < self.SAMPLE_NUM_CUTOFF

    def filter_by_width(self, width: int = None) -> list:
        """Filters a list of tuples, where a tuple contains a width variable"""
        return list(filter(lambda x: x[0] == width, self.data))

    @staticmethod
    def aggregate_from_one_channel(channel_data: list[ChannelData]) -> tuple:
        """Return a list of tuples. Each tuple contains 3 lists: xdata, ydata and yerr from one channel width"""
        # print(f'channel_data: {[channel_datum for channel_datum in channel_data]}')
        xdata = []
        ydata_yerr_aggregated = []
        for channel_datum in channel_data:
            print(f'aggregate from channel_datum: {channel_datum}')
            print(channel_datum.df)
            xdata_, ydata, yerr = channel_datum.get_data()
            if len(xdata_) > len(xdata):
                xdata = xdata_
            print(f'xdata: {xdata}\nydata: {ydata}\nyerr: {yerr}\n')
            ydata_yerr_aggregated.append((ydata, yerr))
        return xdata, ydata_yerr_aggregated

    @staticmethod
    def sort_tuples(data: list, idx_to_sort_by: int = 0) -> list | None:
        if data:
            return data.sort(key=lambda x: x[idx_to_sort_by])
        else:
            return None
