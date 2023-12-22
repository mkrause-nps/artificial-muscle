#!/usr/bin/env python3
import os
from enum import Enum
import matplotlib.pyplot as plt
import pandas
import pandas as pd
from scipy.stats import f_oneway

from src.utilities import Utilities
from src.imagej_analysis.constants import Constants
from src.imagej_analysis.channel_factory import ChannelFactory
from src.imagej_analysis.channel import Channel, Orientation, Material
from src.imagej_analysis.data_aggregator import DataAggregator
from src.imagej_analysis.imagej_csv_loader import ImageJCsvLoader


class FigureColors(Enum):
    ZERO_DEG = 'black'
    NINETY_DEG = 'black'


class DataFrameColumns(Enum):
    FactorA = 'channel'
    FactorB = 'material'
    FactorC = 'orientation'
    Value = 'ratio'


def main():
    # 1. Get a list of all CSV files:
    file_list = ImageJCsvLoader.list_csv_files()

    # 2. Get a list of dictionaries, each of which contains the raw data:
    image_data_raw_items: list[list[dict]] = list(map(ImageJCsvLoader.load, file_list))

    # 3. Create a list of channel objects.
    channels: list[Channel] = ChannelFactory.create_channel_length_instances(imagej_data_raw_items=image_data_raw_items)

    # 4. Create a data aggregator for each data set:
    vertical_sup706 = DataAggregator(channels=channels, material=Material.SUP, orientation=Orientation.VERTICAL)
    horizontal_sup706 = DataAggregator(channels=channels, material=Material.SUP, orientation=Orientation.HORIZONTAL)
    vertical_agilus = DataAggregator(channels=channels, material=Material.Agilus, orientation=Orientation.VERTICAL)
    horizontal_agilus = DataAggregator(channels=channels, material=Material.Agilus, orientation=Orientation.HORIZONTAL)

    data_sets: list[DataAggregator] = [vertical_sup706, horizontal_sup706, vertical_agilus, horizontal_agilus]

    df_all = pd.DataFrame(
        columns=[DataFrameColumns.FactorA.value, DataFrameColumns.FactorB.value, DataFrameColumns.FactorC.value,
                 DataFrameColumns.Value.value])

    # 5. Create scatter plot with error bars
    for data_set in data_sets:
        x, x_error, y, y_error = __get_width_and_height_data(data_set)
        __plot_width_height_data(data_aggregator=data_set, x=x, y=y, x_error=x_error, y_error=y_error,
                                 x_label=Constants.X_LABEL,
                                 y_label=Constants.Y_LABEL)

        x, y, y_error = __get_ratio_data(data_set)
        __plot_ratio_data(data_aggregator=data_set, x=x, y=y, y_error=y_error, x_label=Constants.X_LABEL_RATIO,
                          y_label=Constants.Y_LABEL_RATIO, min_=0, max_=1, title=False)

        __fill_df(df=df_all, data_set=data_set)

    groups_all: list = [df_all[DataFrameColumns.Value.value][
                            (df_all[DataFrameColumns.FactorA.value] == levelA) &
                            (df_all[DataFrameColumns.FactorB.value] == levelB) &
                            (df_all[DataFrameColumns.FactorC.value] == levelC)]
                        for levelA in df_all[DataFrameColumns.FactorA.value].unique()
                        for levelB in df_all[DataFrameColumns.FactorB.value].unique()
                        for levelC in df_all[DataFrameColumns.FactorC.value].unique()
                        ]
    f_statistic, p_value = f_oneway(*groups_all)
    print(f'groups_all: F statistic: {f_statistic}, p-value: {p_value}')

    groups_material_orientation: list = [df_all[DataFrameColumns.Value.value][
                                             (df_all[DataFrameColumns.FactorB.value] == levelB) &
                                             (df_all[DataFrameColumns.FactorC.value] == levelC)]
                                         for levelB in df_all[DataFrameColumns.FactorB.value].unique()
                                         for levelC in df_all[DataFrameColumns.FactorC.value].unique()
                                         ]
    f_statistic, p_value = f_oneway(*groups_material_orientation)
    print(f'groups_orientation_material: F statistic: {f_statistic}, p-value: {p_value}')

    groups_channel: list = [df_all[DataFrameColumns.Value.value][
                                (df_all[DataFrameColumns.FactorA.value] == levelA)]
                            for levelA in df_all[DataFrameColumns.FactorA.value].unique()
                            ]
    f_statistic, p_value = f_oneway(*groups_channel)
    print(f'groups_channel: F statistic: {f_statistic}, p-value: {p_value}')

    __per_channel_width_statistics(df=df_all)


def __plot_width_height_data(data_aggregator: DataAggregator, x: list, y: list, x_error: list, y_error: list,
                             label: str = '', min_: int = Constants.AXIS_MIN, max_: int = Constants.AXIS_MAX,
                             x_label: str = '', y_label: str = '', title: bool = False, legend: bool = False,
                             fmt: str = 'o', capsize: int = 4) -> None:
    plt.errorbar(x, y, xerr=x_error, yerr=y_error, fmt=fmt, capsize=capsize, label=label,
                 color=FigureColors.ZERO_DEG.value, ecolor=FigureColors.ZERO_DEG.value)

    # Set x- and y-axis limits
    plt.xlim(xmin=min_, xmax=max_)
    plt.ylim(ymin=min_, ymax=max_)

    # Add a diagonal line where x equals y
    plt.plot([min_, max_], [min_, max_], linestyle='--', color='gray', label='x=y line')

    # Label each data point with its planned width:
    for i, label in enumerate(Constants.WIDTHS):
        plt.text(x=x[i] + Constants.LABEL_OFFSET_X, y=y[i] + Constants.LABEL_OFFSET_Y, s=label, ha='right', va='bottom',
                 fontsize=9)

    fontsize = 12
    # Set labels and title
    plt.xlabel(x_label, fontsize=fontsize)
    plt.ylabel(y_label, fontsize=fontsize)
    if title:
        plt.title(f'Orientation: {data_aggregator.orientation.value}, Material: {data_aggregator.material.value}')

    plt.gca().set_aspect('equal', adjustable='box')

    # Add a legend
    if legend:
        plt.legend()

    # Set font size for tick labels
    plt.xticks(fontsize=fontsize)  # Adjust the font size for x-axis tick labels
    plt.yticks(fontsize=fontsize)  # Adjust the font size for y-axis tick labels

    # Save the plot to disk in SVG format
    Utilities.ensure_directory_exists(Constants.FIGURE_DIR)
    fig_name = f'{data_aggregator.orientation.value}_{data_aggregator.material}.svg'
    fig_path = os.path.join(Constants.FIGURE_DIR, fig_name)
    plt.savefig(fig_path)

    # Save the plot to disk in JPEG format with high resolution
    fig_name = f'{data_aggregator.orientation.value}_{data_aggregator.material}.png'
    fig_path = os.path.join(Constants.FIGURE_DIR, fig_name)
    plt.savefig(fig_path)

    # Show the plot
    plt.show()


def __plot_ratio_data(data_aggregator: DataAggregator, x: list, y: list, y_error: list,
                      label: str = '', min_: int = Constants.AXIS_MIN, max_: int = Constants.AXIS_MAX,
                      x_label: str = '', y_label: str = '', title: bool = True, legend: bool = False, fmt: str = 'o',
                      capsize: int = 4) -> None:
    plt.errorbar(x, y, yerr=y_error, fmt=fmt, capsize=capsize, label=label,
                 color=FigureColors.ZERO_DEG.value, ecolor=FigureColors.ZERO_DEG.value)

    if title:
        plt.title(f'Orientation: {data_aggregator.orientation.value}, Material: {data_aggregator.material.value}')

    plt.ylim(ymin=min_, ymax=max_)
    fontsize = 12
    # Set labels and title
    plt.xlabel(x_label, fontsize=fontsize)
    plt.ylabel(y_label, fontsize=fontsize)

    plt.gca().set_aspect(2000)

    # Set font size for tick labels
    plt.xticks(fontsize=fontsize)  # Adjust the font size for x-axis tick labels
    plt.yticks(fontsize=fontsize)  # Adjust the font size for y-axis tick labels

    # Save the plot to disk in SVG format
    Utilities.ensure_directory_exists(Constants.FIGURE_DIR)
    fig_name = f'{data_aggregator.orientation.value}_{data_aggregator.material}_ratio.svg'
    fig_path = os.path.join(Constants.FIGURE_DIR, fig_name)
    plt.savefig(fig_path)

    # Save the plot to disk in JPEG format with high resolution
    fig_name = f'{data_aggregator.orientation.value}_{data_aggregator.material}_ratio.png'
    fig_path = os.path.join(Constants.FIGURE_DIR, fig_name)
    plt.savefig(fig_path)

    # Show the plot
    plt.show()


def __get_width_and_height_data(data_aggregator: DataAggregator) -> tuple[list, list, list, list]:
    """Returns x, x_err, y, and y_err of width and height for a channel object."""
    return (data_aggregator.averages_width(), data_aggregator.stdevs_width(), data_aggregator.averages_height(),
            data_aggregator.stdevs_height())


def __get_ratio_data(data_aggregator: DataAggregator) -> tuple[list, list, list]:
    """Returns x, y, and y_err of a channel's aspect ratio."""
    y, y_err = data_aggregator.average_aspect_ratio()
    return Constants.WIDTHS, y, y_err


def __fill_df(df: pandas.DataFrame, data_set: DataAggregator):
    """Fills the dataframe with values from a data set, so it can be used for statistical analysis."""
    for width in Constants.WIDTHS:
        ratios = data_set.get_aspect_ratio(width=width)
        for ratio in ratios:
            df.loc[len(df)] = [width, data_set.material.value, data_set.orientation.value, ratio]


def __per_channel_width_statistics(df: pandas.DataFrame):
    """Calculates the"""
    widths = Constants.WIDTHS
    df_out = pandas.DataFrame(columns=['width (um)', 'F-statistic', 'p-value'])
    for width in widths:
        filtered_df = df[df[DataFrameColumns.FactorA.value] == width]
        print(filtered_df)

        groups: list = [filtered_df[DataFrameColumns.Value.value][
                                (filtered_df[DataFrameColumns.FactorA.value] == levelA) &
                                (filtered_df[DataFrameColumns.FactorB.value] == levelB) &
                                (filtered_df[DataFrameColumns.FactorC.value] == levelC)]
                            for levelA in filtered_df[DataFrameColumns.FactorA.value].unique()
                            for levelB in filtered_df[DataFrameColumns.FactorB.value].unique()
                            for levelC in filtered_df[DataFrameColumns.FactorC.value].unique()
                            ]
        f_statistic, p_value = f_oneway(*groups)
        print(f'groups for width {width}: F-statistic: {f_statistic}, p-value: {p_value}')
        df_out.loc[len(df_out)] = [width, f_statistic, p_value]

    csv_path: str = os.path.join(Constants.DATA_DIR, 'f_statistics.csv')
    Utilities.save_df_to_csv(df=df_out, file_path=csv_path)


if __name__ == '__main__':
    main()
