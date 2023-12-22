#!/usr/bin/env python3
import os
from typing import List


class Constants:
    home_directory = os.path.expanduser("~")
    _data_dir = 'data/ms_revision'
    _figure_dir = 'figures'
    DATA_DIR: str = os.path.join(home_directory, _data_dir)
    FIGURE_DIR: str = os.path.join(home_directory, _data_dir, _figure_dir)
    AXIS_MIN: int = 0
    AXIS_MAX: int = 1200
    WIDTHS: List[int] = [192, 288, 384, 512, 608, 704, 800, 896, 992]
    LABEL_OFFSET_X: int = -32
    LABEL_OFFSET_Y: int = 5
    X_LABEL: str = 'Measured channel width ($\mu m$)'
    Y_LABEL: str = 'Measured channel height ($\mu m$)'
    X_LABEL_RATIO: str = 'Planned channel width ($\mu m$)'
    Y_LABEL_RATIO: str = 'Channel (height / width) ratio'