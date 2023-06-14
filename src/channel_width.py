#!/usr/bin/env python3

import numpy
import pandas as pd
from src.config import Config


class ChannelWidth:

    def __init__(self, dataframe: pd.DataFrame, prior: dict, past: dict):
        self.df: pd.DataFrame = dataframe
        self.prior: dict = prior
        self.past: dict = past
        self.differences: pd.DataFrame = pd.DataFrame()
        self.widths: pd.DataFrame = pd.DataFrame()
        self.relative_error: pd.DataFrame = pd.DataFrame()

    def get_relative_error(self) -> None:
        """Get the relative error for each set width and its standard deviation"""
        df = self.__get_rel_err(time_measured=self.prior)
        # Add the relative error for each value to dataframe.
        df['rel_err'] = (df['widths_um'] - df['channel_id']) / df['channel_id'] * 100
        data = {
            'channel_id': self.__get_id_column(),
            'rel_err_means': self.__get_mean(df=df, key_to_group_by='channel_id', col_to_get_mean='rel_err'),
            'rel_err_stdevs': self.__get_stdev(df=df, key_to_group_by='channel_id', col_to_get_mean='rel_err')
        }
        self.relative_error = pd.DataFrame(data=data, columns=list(data.keys()))
        self.relative_error.reset_index(drop=True, inplace=True)

    def get_widths(self) -> None:
        """Get widths and the error (standard deviation)"""
        data = {
            'channel_id': self.__get_id_column(),
            'width_prior': self.__get_means(time_measured=self.prior),
            'width_prior_err': self.__get_stdevs(time_measured=self.prior),
            'width_past': self.__get_means(time_measured=self.past),
            'width_past_err': self.__get_stdevs(time_measured=self.past),
        }
        self.widths = pd.DataFrame(data=data, columns=list(data.keys()))
        self.widths.reset_index(drop=True, inplace=True)

    def get_differences(self) -> None:
        """Differences of channel width (in um) measured under two conditions."""
        self.differences = pd.DataFrame(
            data={
                'channel_id': self.__get_id_column(),
                'width_diff': self.__get_means(time_measured=self.past) - self.__get_means(time_measured=self.prior)
            },
            columns=['channel_id', 'width_diff']
        )
        self.differences.reset_index(drop=True, inplace=True)  # not sure why the index was messed but this fixes it

    def get_fractional_differences(self) -> None:
        width_frac_diff = (self.__get_means(time_measured=self.past) / self.__get_means(time_measured=self.prior)) * 100
        self.differences = pd.DataFrame(
            data={
                'channel_id': self.__get_id_column(),
                'width_frac_diff': width_frac_diff
            },
            columns=['channel_id', 'width_frac_diff']
        )
        self.differences.reset_index(drop=True, inplace=True)

    def get_fractional_differences2(self) -> None:
        after = self.__get_means(time_measured=self.past)
        before = self.__get_means(time_measured=self.prior)
        width_frac_diff = ((after - before) / before) * 100

        propagated_err = self.__get_propagated_error()

        self.differences = pd.DataFrame(
            data={
                'channel_id': self.__get_id_column(),
                'width_frac_diff': width_frac_diff,
                'width_err': propagated_err
            },
            columns=['channel_id', 'width_frac_diff', 'width_err']
        )
        self.differences.reset_index(drop=True, inplace=True)

    def __get_propagated_error(self) -> pd.Series:
        """Return the propagated error (described in document in one of the directories)."""
        after = self.__get_means(time_measured=self.past)
        before = self.__get_means(time_measured=self.prior)
        after_err = self.__get_stdevs(time_measured=self.past)
        before_err = self.__get_stdevs(time_measured=self.prior)

        propagated_err = ((after_err / before**2) + (before_err * after**2 / before**4)) * 100

        return propagated_err

    def __filter_df(self, mask: dict) -> pd.DataFrame:
        """Filter dataframe on three columns of interest and return as new df"""
        return self.df.loc[
            (self.df['status'] == mask['status']) &
            (self.df['print_direction'] == mask['print_direction']) &
            (self.df['material'] == mask['material'])
            ]

    def __get_data(self, time_measured: dict) -> pd.DataFrame:
        return self.__filter_df(mask=time_measured)

    def __get_means(self, time_measured: dict) -> pd.Series:
        """Get the means for the aggregated channel IDs and return as pandas series."""
        return self.__get_mean(
            df=self.__get_data(time_measured=time_measured),
            key_to_group_by='channel_id',
            col_to_get_mean=Config.measured_widths_col_name
        )

    def __get_stdevs(self, time_measured: dict) -> pd.Series:
        """Get the standard deviations for the aggregated channel IDs and return as pandas series."""
        return self.__get_stdev(
            df=self.__get_data(time_measured=time_measured),
            key_to_group_by='channel_id',
            col_to_get_mean=Config.measured_widths_col_name
        )

    @staticmethod
    def __get_mean(df: pd.DataFrame, key_to_group_by: str, col_to_get_mean: str) -> pd.Series:
        """Return the mean of chip IDs for a given status, print direction, material, and channel ID"""
        grouped: pd.SeriesGroupBy = df[col_to_get_mean].groupby(df[key_to_group_by])
        return grouped.mean()

    @staticmethod
    def __get_stdev(df: pd.DataFrame, key_to_group_by: str, col_to_get_mean: str) -> pd.Series:
        """Return the standard deviation of chip IDs for a given status, print direction, material, and channel ID"""
        grouped = df[col_to_get_mean].groupby(df[key_to_group_by])
        return grouped.std()

    def __get_id_column(self) -> numpy.ndarray:
        """Add the channel ID as a column, assign unique names to columns and combine data from two DFs into one."""
        return self.df['channel_id'].unique()  # get a set of IDs

    def __get_rel_err(self, time_measured:dict):
        df = self.__get_data(time_measured=time_measured)
        return df
