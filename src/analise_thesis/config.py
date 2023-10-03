#!/usr/bin/env python3

from enum import Enum


class ChipType(Enum):
    HARD = 1
    SOFT = 2


class Config:
    """Configuration parameters specific to the system where data are processed and analyzed."""
    COLUMN_NAME_CHIP = 'Chip Name'
    COLUMN_NAME_AVG_RESISTANCE = 'Resistance (kΩ)'
    COLUMN_NAME_STDEV_RESISTANCE = 'Standard Deviation (kΩ)'

    SI_UNIT = 'k$\\Omega$'
    excel_spreadsheet_path: str = '/home/mkrause/data/artificial-muscle/analise_thesis'
    spreadsheet_filename: str = 'CNF Data.xlsx'
    sheet_name_affix: str = ' Channel Data'
    chip_type_selector: dict = {
        'soft': ChipType.SOFT.name.lower(),
        'hard': ChipType.HARD.name.lower()
    }
