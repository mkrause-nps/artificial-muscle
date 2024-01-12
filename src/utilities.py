#!/usr/bin/env python3

import os
from enum import Enum

import pandas as pd


class Utilities:

    @staticmethod
    def get_filename_from_path(absolute_file_path: str):
        return os.path.splitext(os.path.basename(absolute_file_path))[0]

    @staticmethod
    def get_project_root() -> str:
        """Get the absolute path of the project root."""
        current_path = os.path.abspath(__file__)  # Get the absolute path of the current script
        project_root = os.path.dirname(os.path.dirname(current_path))  # Go up two levels to reach the project root
        return project_root

    @staticmethod
    def get_filename_list(start_path: str) -> list[str]:
        """Get a list of all absolute filenames, recursively, from directory start_path."""
        file_list: list = []
        for root, dirs, files in os.walk(start_path):
            for file in files:
                file_list.append(os.path.join(root, file))

        return file_list

    @classmethod
    def ensure_directory_exists(cls, directory_path):
        if not os.path.exists(directory_path):
            os.makedirs(directory_path)
            print(f"Directory '{directory_path}' created.")

    @classmethod
    def save_df_to_csv(cls, df: pd.DataFrame, file_path: str) -> None:
        """Saves a pandas dataframe to a csv file in the specified data directory."""
        df.to_csv(file_path)


class FigureColors(Enum):
    ZERO_DEG = 'black'
    NINETY_DEG = 'black'


class DataFrameColumns(Enum):
    FactorA = 'channel'
    FactorB = 'material'
    FactorC = 'orientation'
    Value = 'ratio'
