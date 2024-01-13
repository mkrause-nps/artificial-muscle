#!/usr/bin/env python3
import pandas as pd

from src.imagej_analysis.channel import Channel, Orientation, Material
from src.imagej_analysis.channel_factory import ChannelFactory
from src.imagej_analysis.imagej_csv_loader import ImageJCsvLoader
from utilities import Utilities
from src.amscope_excel_loader import AmScopeExcelLoader
from src.imagej_analysis.constants import Constants
from src.channel_amscope import ChannelAmScope

CHIP_STATUS = 'past'


def main():
    excel_filename_path = Constants.DATA_DIR_AMSCOPE
    data_amscope: list[dict] = AmScopeExcelLoader.load(filename=excel_filename_path)
    # print(data_amscope)
    df: pd.DataFrame = pd.json_normalize(data_amscope)
    # print(df.head())

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

    # Define a filter for plot:
    df_single_type: pd.DataFrame = df.loc[
        (df['status'] == CHIP_STATUS) &
        (df['print_direction'] == channel_types['perp_ref_mat'][0]) &
        (df['material'] == channel_types['para_ref_mat'][1]) &
        (df['channel_id'] != 64) &
        (df['channel_id'] != 96)
        ]
    # print(df_single_type)

    # Create a list of tuples for one channel type for AmScope images:
    x_bar_widths_amscope: list[tuple] = []
    for width in Constants.WIDTHS:
        df_ = df_single_type.loc[df_single_type['channel_id'] == width]
        channel_amscope: ChannelAmScope = ChannelAmScope(data=df_)
        # print(channel)
        x_bar_widths_amscope.append(
            (channel_amscope.planned_width, channel_amscope.get_average_width(), channel_amscope.get_stdev_width()))
    # print(x_bar_widths)

    # Define a filter for plot:
    filter_: dict = {
        'orientation': Orientation.VERTICAL,
        'material': Material.Agilus
    }

    # Create a list of tuples for one channel type for ImageJ images:
    x_bar_widths_imagej: list[tuple] = []
    for channel_imagej in channels_imagej:
        if channel_imagej.material == filter_.get('material') and channel_imagej.orientation == filter_.get('orientation'):
            x_bar_widths_imagej.append((channel_imagej.planned_width, channel_imagej.get_average_width(), channel_imagej.get_stdev_width()))
    x_bar_widths_imagej.sort(key=lambda tup: tup[0])
    print(x_bar_widths_imagej)  # ToDo: the list contains 5 samples of each width, those need to be averaged before
    # we can create the plots


if __name__ == '__main__':
    main()
