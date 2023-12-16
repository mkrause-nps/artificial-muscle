#!/usr/bin/env python3
import matplotlib.pyplot as plt

from src.imagej_analysis.channel_factory import ChannelFactory
from src.imagej_analysis.channel import Channel, Orientation, Material
from src.imagej_analysis.data_aggregator import DataAggregator
from src.imagej_analysis.imagej_csv_loader import ImageJCsvLoader


def main():
    # 1. Get a list of all CSV files:
    file_list = ImageJCsvLoader.list_csv_files()
    image_data_raw_items: list[list[dict]] = list(map(ImageJCsvLoader.load, file_list))
    channels: list[Channel] = ChannelFactory.create_channel_length_instances(imagej_data_raw_items=image_data_raw_items)
    counter: int = 0
    # for channel in channels:
    #     print(f'channel count: {counter}')
    #     counter += 1
    #     print(channel)
    vertical_sup706 = DataAggregator(channels=channels, material=Material.SUP, orientation=Orientation.VERTICAL)
    # for item in vertical_sup706.data:
    #     print(f'channel count: {counter}')
    #     counter += 1
    #     print(item)
    # print(f'total channels: {len(vertical_sup706)}')
    # print(vertical_sup706.averages_width())
    # print(vertical_sup706.stdevs_width())
    # print(vertical_sup706.averages_height())
    # print(vertical_sup706.stdevs_height())

    x = vertical_sup706.averages_width()
    x_error = vertical_sup706.stdevs_width()
    y = vertical_sup706.averages_height()
    y_error = vertical_sup706.stdevs_height()

    # Create scatter plot with error bars
    plt.errorbar(x, y, xerr=x_error, yerr=y_error, fmt='o', capsize=4, label='Data with Error Bars')

    # Set x and y axis limits
    min_ = 0
    max_ = 1000
    plt.xlim(xmin=min_, xmax=max_)
    plt.ylim(ymin=min_, ymax=max_)

    # Add a diagonal line where x equals y
    plt.plot([min_, max_], [min_, max_], linestyle='--', color='gray', label='x=y line')

    # Set labels and title
    plt.xlabel('Channel width ($\mu m$)')
    plt.ylabel('Channel height ($\mu m$)')
    plt.title(f'Orientation: {vertical_sup706.orientation.value}, Material: {vertical_sup706.material.value}')

    plt.gca().set_aspect('equal', adjustable='box')

    # Add a legend
    plt.legend()

    # Show the plot
    plt.show()


if __name__ == '__main__':
    main()
