#!/usr/bin/env python3

import csv
from src.utilities import Utilities


class ImageJCsvLoader(object):
    """Loads data from a CSV file into a list of dictionaries. Each dictionary has the following: item number,
    file name, length of channel. The length of the channel is the vertical dimension if the item number is less than
    4, and is otherwise the horizontal dimension.
    """
    header_item_number = 'item_number'
    header_label = 'Label'
    header_length = 'Length'
    headers = [header_item_number, header_label, header_length]
    filename = None

    @classmethod
    def load(cls, filename: str) -> list[dict]:
        with open(filename, 'r') as fp:
            reader = csv.reader(fp)
            fieldnames_ = next(reader)
            is_label = cls.header_label in fieldnames_
            conditions: list[bool] = cls._filter_fieldnames(fieldnames_)
            rows = []
            for row in reader:
                row_ = cls._filter_row(row, conditions=conditions)
                if not is_label:
                    row_ = cls.__append_label_to_row(row=row_, filename=filename)
                rows.append(dict(zip(cls.headers, row_)))

        return rows

    @classmethod
    def filter_filelist(cls, filelist: list) -> list:
        """Filters filelist to contain only CSV files."""
        return [file for file in filelist if file.endswith('.csv')]

    @classmethod
    def _filter_fieldnames(cls, fieldnames_: list) -> list[bool]:
        fieldnames = [True if header in [cls.header_label, cls.header_length] else False for header in fieldnames_]
        fieldnames[0] = True
        return fieldnames

    @staticmethod
    def _filter_row(row: list, conditions: list[bool]) -> list:
        return [item for item, condition in zip(row, conditions) if condition]

    @staticmethod
    def __append_label_to_row(row: list, filename: str) -> list:
        filename_only = Utilities.get_filename_from_path(absolute_file_path=filename)
        row.insert(1, filename_only)
        return row

