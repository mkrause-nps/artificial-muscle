#!/usr/bin/env python3
from src.imagej_analysis.channel import Channel
from src.imagej_analysis.channel_factory import ChannelFactory
from src.imagej_analysis.imagej_csv_loader import ImageJCsvLoader
from utilities import Utilities
from src.amscope_excel_loader import AmScopeExcelLoader
from src.imagej_analysis.constants import Constants


def main():
    excel_filename_path = Constants.DATA_DIR_AMSCOPE
    data_amscope = AmScopeExcelLoader.load(filename=excel_filename_path)
    print(data_amscope)

    file_list = ImageJCsvLoader.list_csv_files()

    # 2. Get a list of dictionaries, each of which contains the raw data:
    image_data_raw_items: list[list[dict]] = list(map(ImageJCsvLoader.load, file_list))

    # 3. Create a list of channel objects.
    channels: list[Channel] = ChannelFactory.create_channel_length_instances(imagej_data_raw_items=image_data_raw_items)


if __name__ == '__main__':
    main()
