#!/usr/bin/env python3
import pandas as pd

from src.imagej_analysis.channel import Channel
from src.imagej_analysis.channel_factory import ChannelFactory
from src.imagej_analysis.imagej_csv_loader import ImageJCsvLoader
from utilities import Utilities
from src.amscope_excel_loader import AmScopeExcelLoader
from src.imagej_analysis.constants import Constants


def main():
    excel_filename_path = Constants.DATA_DIR_AMSCOPE
    data_amscope: list[dict] = AmScopeExcelLoader.load(filename=excel_filename_path)
    # print(data_amscope)
    df: pd.DataFrame = pd.json_normalize(data_amscope)
    # print(df.head())

    # file_list = ImageJCsvLoader.list_csv_files()
    #
    # # 2. Get a list of dictionaries, each of which contains the raw data:
    # image_data_raw_items: list[list[dict]] = list(map(ImageJCsvLoader.load, file_list))
    #
    # # 3. Create a list of channel objects.
    # channels: list[Channel] = ChannelFactory.create_channel_length_instances(imagej_data_raw_items=image_data_raw_items)
    #
    # for channel in channels:
    #     print(channel)

    # This is hacky. Better would be to define a bunch of enums that contain that info...
    figure_types: dict[str, list[str]] = {
        'perp_sac_mat': ['perpendicular', 'sacrificial_material'],
        'perp_ref_mat': ['perpendicular', 'black_resin'],
        'para_sac_mat': ['parallel', 'sacrificial_material'],
        'para_ref_mat': ['parallel', 'black_resin']
    }

    df_single_type: pd.DataFrame = df.loc[
        (df['status'] == 'past') &
        (df['print_direction'] == figure_types['perp_ref_mat'][0]) &
        (df['material'] == figure_types['para_ref_mat'][1]) &
        (df['channel_id'] != 64) &
        (df['channel_id'] != 96)
        ]
    print(df_single_type)


if __name__ == '__main__':
    main()
