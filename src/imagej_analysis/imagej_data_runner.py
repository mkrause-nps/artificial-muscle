#!/usr/bin/env python3
import os

from src.imagej_analysis.channel import Channel
from src.imagej_analysis.imagej_csv_loader import ImageJCsvLoader


home_directory = os.path.expanduser("~")
data_dir = 'data/ms_revision/vp/01'
DATA_DIR = os.path.join(home_directory, data_dir)


def main():
    file_list = ImageJCsvLoader.filter_filelist(os.listdir(DATA_DIR))
    for file in file_list:
        imagej_data_raw = ImageJCsvLoader.load(filename=os.path.join(DATA_DIR, file))
        channel = Channel(imagej_data_raw)
        print(channel)


if __name__ == '__main__':
    main()
