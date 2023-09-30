#!/usr/bin/env python3

import os
import pandas as pd


class Loader:

    @classmethod
    def read_data(cls, data_path: str, sheet_name: str) -> pd.DataFrame | None:
        """
        Read a specific sheet of an Excel spreadsheet file and return the data as a Pandas Dataframe object.
        data_path -- the absolute path to an Excel spreadsheet
        sheet_name -- the name of the sheet in that spreadsheet file
        """
        data_filename: str = cls.__get_data_filename(data_path=data_path)
        if data_filename is None:
            return None

        df = pd.read_excel(data_filename, sheet_name=sheet_name)
        df.dropna(axis='rows', how='all', inplace=True)  # remove all rows where all values are NaN's
        df.fillna(method='ffill', inplace=True)          # repeat the last value (from top) if followed by a NaN
        df.dropna(axis='columns', inplace=True)          # drop columns that have at least one NaN
        idx = pd.Index(pd.RangeIndex(start=0, stop=len(df), step=1))
        df.set_index(keys=pd.Index(idx), inplace=True)   # generate index and re-index df
        return df.astype({'Injection Number': 'int'})    # cast injection numbers of `int`

    @staticmethod
    def write_to_json(df: pd.DataFrame, dst: str) -> None:
        """Exports Pandas Dataframe to JSON file."""
        abs_fname = os.path.join(dst, 'exported_dataframe.json')
        df.to_json(abs_fname)

    @staticmethod
    def __get_data_filename(data_path: str, data_filename: str = None) -> str | None:
        if not data_filename:
            try:
                data_filename = os.listdir(data_path)[0]
            except FileNotFoundError as err:
                print(err.errno)
                return None
        return os.path.join(data_path, data_filename)
