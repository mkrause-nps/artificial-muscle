#!/usr/bin/env python3
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from src.config import Config


class ExperimentSpecs:

    # df_current1: pd.DataFrame = None
    # df_current2: pd.DataFrame = None
    #
    # current1_stats: float = None
    # current2_stats: float = None

    # perp_before_sm = {
    #     'status': 'prior',
    #     'print_direction': 'perpendicular',
    #     'material': 'sacrificial_material'
    # }
    #
    # perp_before_br = {
    #     'status': 'prior',
    #     'print_direction': 'perpendicular',
    #     'material': 'black_resin'
    # }
    #
    # perp_after_sm = {
    #     'status': 'past',
    #     'print_direction': 'perpendicular',
    #     'material': 'sacrificial_material'
    # }
    #
    # perp_after_br = {
    #     'status': 'past',
    #     'print_direction': 'perpendicular',
    #     'material': 'black_resin'
    # }
    #
    # para_before_sm = {
    #     'status': 'prior',
    #     'print_direction': 'parallel',
    #     'material': 'sacrificial_material'
    # }
    #
    # para_before_br = {
    #     'status': 'prior',
    #     'print_direction': 'parallel',
    #     'material': 'black_resin'
    # }
    #
    # para_after_sm = {
    #     'status': 'past',
    #     'print_direction': 'parallel',
    #     'material': 'sacrificial_material'
    # }
    #
    # para_after_br = {
    #     'status': 'past',
    #     'print_direction': 'parallel',
    #     'material': 'black_resin'
    # }

    def __init__(self, dataframe: pd.DataFrame, prior: dict, past: dict):
        self.df: pd.DataFrame = dataframe
        self.prior: dict = prior
        self.past: dict = past
        self.differences: pd.DataFrame = pd.DataFrame()

    def get_differences(self):
        """Differences of measured channel width (in um) between two measurement times."""
        self.differences = pd.DataFrame(
            data={
                'channel_id': self.__get_id_column(),
                'width_diff': self.__get_stats(time_measured=self.past) - self.__get_stats(time_measured=self.prior)
            },
            columns=['channel_id', 'width_diff']
        )

    def plot_differences(self):
        title = f'Channel widths {self.prior["material"]}: {self.past["status"]} - {self.prior["status"]}'
        xlabel = 'channel ID'
        ylabel = r'width difference ($\mu$m)'

        # Create plot.
        plt.plot(self.differences['channel_id'], self.differences['width_diff'])
        plt.title(title)

        plt.show()

    def __filter_df(self, mask: dict) -> pd.DataFrame:
        """Filter dataframe for two quantities of interest and return as new df"""
        return self.df.loc[
            (self.df['status'] == mask['status']) &
            (self.df['print_direction'] == mask['print_direction']) &
            (self.df['material'] == mask['material'])
            ]

    def __get_data(self, time_measured: dict) -> pd.DataFrame:
        return self.__filter_df(mask=time_measured)

    def __get_stats(self, time_measured: dict) -> pd.Series:
        """Get the means for the aggregated channel IDs and return as pandas series."""
        return self.__get_mean(
            df=self.__get_data(time_measured=time_measured),
            key_to_group_by='channel_id',
            col_to_get_mean=Config.measured_widths_col_name
        )

    @staticmethod
    def __get_mean(df: pd.DataFrame, key_to_group_by: str, col_to_get_mean) -> pd.Series:
        grouped = df[col_to_get_mean].groupby(df[key_to_group_by])
        return grouped.mean()

    def __get_id_column(self) -> pd.Series:
        """Add the channel ID as a column, assign unique names to columns and combine data from two DFs into one."""
        return self.df['channel_id'].unique()  # get a set of IDs
