#!/usr/bin/env python3
import os

import pandas as pd
from matplotlib import pyplot as plt

from src.imagej_analysis.channel import Channel, Orientation, Material
from src.imagej_analysis.channel_factory import ChannelFactory
from src.imagej_analysis.imagej_csv_loader import ImageJCsvLoader
from utilities import Utilities, FigureColors
from src.amscope_excel_loader import AmScopeExcelLoader
from src.imagej_analysis.constants import Constants
from src.channel_amscope import ChannelAmScope

CHIP_STATUS = 'past'
NAME_PREFIX = 'width_vs_width'


def main():
    excel_filename_path = Constants.DATA_DIR_AMSCOPE
    data_amscope: list[dict] = AmScopeExcelLoader.load(filename=excel_filename_path)
    df: pd.DataFrame = pd.json_normalize(data_amscope)

    file_list = ImageJCsvLoader.list_csv_files()

    # 2. Get a list of dictionaries, each of which contains the raw data:
    image_data_raw_items: list[list[dict]] = list(map(ImageJCsvLoader.load, file_list))

    # 3. Create a list of channel objects.
    channels_imagej: list[Channel] = ChannelFactory.create_channel_length_instances(
        imagej_data_raw_items=image_data_raw_items)

    # for channel_imagej in channels_imagej:
    #     print(channel_imagej)

    # This is hacky. Better would be to define a bunch of enums that contain that info...
    channel_types: dict[str, list[str]] = {
        'perp_sac_mat': ['perpendicular', 'sacrificial_material'],
        'perp_ref_mat': ['perpendicular', 'black_resin'],
        'para_sac_mat': ['parallel', 'sacrificial_material'],
        'para_ref_mat': ['parallel', 'black_resin']
    }

    ###################################################
    # PLOT 1: PERPENDICULAR, SACRIFICIAL MATERIAL
    ###################################################
    figure_name = 'perpendicular_sacrificialMaterial'
    # Define a filter to plot AmScope data:
    df_single_type: pd.DataFrame = df.loc[
        (df['status'] == CHIP_STATUS) &
        (df['print_direction'] == channel_types['perp_sac_mat'][0]) &
        (df['material'] == channel_types['perp_sac_mat'][1]) &
        (df['channel_id'] != 64) &
        (df['channel_id'] != 96)
        ]

    # Define a filter to plot ImageJ data:
    filter_: dict = {
        'orientation': Orientation.HORIZONTAL,
        'material': Material.SUP
    }

    # Get data for specs:
    x_bar_widths_amscope = get_amscope_plot_data(df_single_type=df_single_type)
    x_bar_widths_imagej = get_imagej_plot_data(channels_imagej=channels_imagej, filter=filter_)

    # Create plots:
    x, y, x_err, y_err = get_x_y_x_err_y_err(imagej_data=x_bar_widths_imagej, amscope_data=x_bar_widths_amscope)
    __plot_width_against_width_data(x=x, y=y, x_error=x_err, y_error=y_err, fname=figure_name )

    ###################################################
    # PLOT 2: PERPENDICULAR, BLACK MATERIAL
    ###################################################
    figure_name = 'perpendicular_blackMaterial'
    # Define a filter to plot AmScope data:
    df_single_type: pd.DataFrame = df.loc[
        (df['status'] == CHIP_STATUS) &
        (df['print_direction'] == channel_types['perp_ref_mat'][0]) &
        (df['material'] == channel_types['perp_ref_mat'][1]) &
        (df['channel_id'] != 64) &
        (df['channel_id'] != 96)
        ]

    # Define a filter to plot ImageJ data:
    filter_: dict = {
        'orientation': Orientation.HORIZONTAL,
        'material': Material.Agilus
    }

    # Get data for specs:
    x_bar_widths_amscope = get_amscope_plot_data(df_single_type=df_single_type)
    x_bar_widths_imagej = get_imagej_plot_data(channels_imagej=channels_imagej, filter=filter_)

    # Create plots:
    x, y, x_err, y_err = get_x_y_x_err_y_err(imagej_data=x_bar_widths_imagej, amscope_data=x_bar_widths_amscope)
    __plot_width_against_width_data(x=x, y=y, x_error=x_err, y_error=y_err, fname=figure_name )

    ###################################################
    # PLOT 3: PARALLEL, SACRIFICIAL MATERIAL
    ###################################################
    figure_name = 'parallel_sacrificialMaterial'
    # Define a filter to plot AmScope data:
    df_single_type: pd.DataFrame = df.loc[
        (df['status'] == CHIP_STATUS) &
        (df['print_direction'] == channel_types['para_sac_mat'][0]) &
        (df['material'] == channel_types['para_sac_mat'][1]) &
        (df['channel_id'] != 64) &
        (df['channel_id'] != 96)
        ]

    # Define a filter to plot ImageJ data:
    filter_: dict = {
        'orientation': Orientation.VERTICAL,
        'material': Material.SUP
    }

    # Get data for specs:
    x_bar_widths_amscope = get_amscope_plot_data(df_single_type=df_single_type)
    x_bar_widths_imagej = get_imagej_plot_data(channels_imagej=channels_imagej, filter=filter_)

    # Create plots:
    x, y, x_err, y_err = get_x_y_x_err_y_err(imagej_data=x_bar_widths_imagej, amscope_data=x_bar_widths_amscope)
    __plot_width_against_width_data(x=x, y=y, x_error=x_err, y_error=y_err, fname=figure_name)

    ###################################################
    # PLOT 4: PARALLEL, BLACK MATERIAL
    ###################################################
    figure_name = 'parallel_blackMaterial'
    # Define a filter to plot AmScope data:
    df_single_type: pd.DataFrame = df.loc[
        (df['status'] == CHIP_STATUS) &
        (df['print_direction'] == channel_types['para_ref_mat'][0]) &
        (df['material'] == channel_types['para_ref_mat'][1]) &
        (df['channel_id'] != 64) &
        (df['channel_id'] != 96)
        ]

    # Define a filter to plot ImageJ data:
    filter_: dict = {
        'orientation': Orientation.VERTICAL,
        'material': Material.Agilus
    }

    # Get data for specs:
    x_bar_widths_amscope = get_amscope_plot_data(df_single_type=df_single_type)
    x_bar_widths_imagej = get_imagej_plot_data(channels_imagej=channels_imagej, filter=filter_)

    # Create plots:
    x, y, x_err, y_err = get_x_y_x_err_y_err(imagej_data=x_bar_widths_imagej, amscope_data=x_bar_widths_amscope)
    __plot_width_against_width_data(x=x, y=y, x_error=x_err, y_error=y_err, fname=figure_name)


def get_x_y_x_err_y_err(imagej_data: list[tuple], amscope_data: list[tuple]) -> tuple:
    """Get data for plot"""
    x = [tup[1] for tup in imagej_data]
    x_err = [tup[2] for tup in imagej_data]

    y = [tup[1] for tup in amscope_data]
    y_err = [tup[2] for tup in amscope_data]

    return x, y, x_err, y_err


def get_amscope_plot_data(df_single_type: pd.DataFrame) -> list[tuple]:
    """Create a list of tuples for one channel type for AmScope images"""
    x_bar_widths_amscope: list[tuple] = []
    for width in Constants.WIDTHS:
        df_ = df_single_type.loc[df_single_type['channel_id'] == width]
        channel_amscope: ChannelAmScope = ChannelAmScope(data=df_)
        x_bar_widths_amscope.append(
            (channel_amscope.planned_width, channel_amscope.get_average_width(), channel_amscope.get_stdev_width()))

    return x_bar_widths_amscope


def get_imagej_plot_data(channels_imagej: list[Channel], filter: dict) -> list[tuple]:
    # Create a list of tuples for one channel type for ImageJ images:
    x_bar_widths_imagej: list[tuple] = []
    for channel_imagej in channels_imagej:
        if channel_imagej.material == filter.get('material') and channel_imagej.orientation == filter.get(
                'orientation'):
            x_bar_widths_imagej.append(
                (channel_imagej.planned_width, channel_imagej.get_average_width(), channel_imagej.get_stdev_width()))
    x_bar_widths_imagej.sort(key=lambda tup: tup[0])

    return average_tuples(tups=x_bar_widths_imagej)


def filter_tuples(tups: list[tuple], width_: int) -> list[tuple]:
    """Return a list of tuples where each tuple if of same width"""
    return [tup for tup in tups if tup[0] == width_]


def average_tuples(tups: list[tuple]) -> list[tuple]:
    """Return a list of tuples where each tuple has a unique width
    Parameters
    @tups: list of tuples where multiple tuples have the same width
    Returns
    @out_tup: list of tuples where each tuple has a unique width
    """
    out_tup: list[tuple] = []
    for width in Constants.WIDTHS:
        tups_of_width: list[tuple] = filter_tuples(tups=tups, width_=width)
        widths = [tup[1] for tup in tups_of_width]
        avg = (sum(widths) / len(tups_of_width))
        widths_err = [tup[2] for tup in tups_of_width]
        stdev = (sum(widths_err) / len(tups_of_width))
        out_tup.append((width, avg, stdev))
    return out_tup


def __plot_width_against_width_data(x: list, y: list, x_error: list, y_error: list,
                                    label: str = '', min_: int = 0, max_: int = 1600,
                                    x_label: str = 'Channel width from cross-cut view ($\mu m$)',
                                    y_label: str = 'Channel width from topview ($\mu m$)',
                                    fname: str = '', legend: bool = False,
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

    plt.gca().set_aspect('equal', adjustable='box')

    # Add a legend
    if legend:
        plt.legend()

    # Set font size for tick labels
    plt.xticks(fontsize=fontsize)  # Adjust the font size for x-axis tick labels
    plt.yticks(fontsize=fontsize)  # Adjust the font size for y-axis tick labels

    # Save the plot to disk in SVG format
    Utilities.ensure_directory_exists(Constants.FIGURE_DIR)
    fig_name = f'{NAME_PREFIX}_{fname}.svg'
    fig_path = os.path.join(Constants.FIGURE_DIR, fig_name)
    plt.savefig(fig_path)

    # Save the plot to disk in JPEG format with high resolution
    fig_name = f'{NAME_PREFIX}_{fname}.png'
    fig_path = os.path.join(Constants.FIGURE_DIR, fig_name)
    plt.savefig(fig_path)

    # Show the plot
    plt.show()


if __name__ == '__main__':
    main()
