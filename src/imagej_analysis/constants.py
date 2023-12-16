#!/usr/bin/env python3
import os


class Constants:
    home_directory = os.path.expanduser("~")
    _data_dir = 'data/ms_revision'
    DATA_DIR = os.path.join(home_directory, _data_dir)
