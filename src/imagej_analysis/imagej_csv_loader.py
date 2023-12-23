#!/usr/bin/env python3

import csv

from src.loader_interface import LoaderInterface
from src.utilities import Utilities
from src.imagej_analysis.constants import Constants


class ColumnHeaders:
    """CSV file column headers of interest."""
    item_number = 'item_number'
    label = 'Label'
    length = 'Length'


class ImageJCsvLoader(LoaderInterface):
    """Loads data from a CSV file into a list of dictionaries. Each dictionary has the following: item number,
    file name, length of channel. The length of the channel is the vertical dimension if the item number is less than
    4, and is otherwise the horizontal dimension.
    """
    COMMON_DATA_DIR = Constants.DATA_DIR
    DATA_EXTENSION = ".csv"
    headers = [ColumnHeaders.item_number, ColumnHeaders.label, ColumnHeaders.length]
    filename = None

    @classmethod
    def load(cls, filename: str) -> list[dict]:
        with open(filename, 'r') as fp:
            reader = csv.reader(fp)
            fieldnames_ = next(reader)
            is_label = ColumnHeaders.label in fieldnames_
            conditions: list[bool] = cls.__filter_fieldnames(fieldnames_)
            rows = []
            for row in reader:
                row_ = cls.__filter_row(row, conditions=conditions)
                if not is_label:
                    row_ = cls.__append_label_to_row(row=row_, filename=filename)
                rows.append(dict(zip(cls.headers, row_)))

        return rows

    @classmethod
    def __filter_fieldnames(cls, fieldnames_: list) -> list[bool]:
        fieldnames = [True if header in [ColumnHeaders.label, ColumnHeaders.length] else False for header in fieldnames_]
        fieldnames[0] = True
        return fieldnames

    @staticmethod
    def __filter_row(row: list, conditions: list[bool]) -> list:
        return [item for item, condition in zip(row, conditions) if condition]

    @staticmethod
    def __append_label_to_row(row: list, filename: str) -> list:
        filename_only = Utilities.get_filename_from_path(absolute_file_path=filename)
        row.insert(1, filename_only)
        return row

    @classmethod
    def list_csv_files(cls) -> list[str]:
        """Returns a list of csv filenames."""
        file_list = Utilities.get_filename_list(start_path=cls.COMMON_DATA_DIR)
        return [file for file in file_list if file.endswith(cls.DATA_EXTENSION)]
