#!/usr/bin/env python3

import os
import logging
import argparse
from enum import Enum
from src.config import Config
from src.figure import Figure

logging.basicConfig(level=logging.INFO)


class Type(Enum):
    """User specifies the type of data to be plotted on command line."""
    image = 'image'
    conductivity = 'conductivity'

    def __str__(self):
        return self.value


parser = argparse.ArgumentParser(description="Artificial Muscle Project")
parser.add_argument('filename', type=str, help='Path to the Excel file')
parser.add_argument('type', type=Type, choices=list(Type), help='Type of data to plot')
args = parser.parse_args()

filename = os.path.join(Config.output_dir, args.filename)

logging.info(f'file name: {filename}')
logging.info(f'data type to process: {args.type}')

_, ax = Figure.figure_handle()
if args.type == Type.conductivity:
    Figure.plot(excel_filename=filename, ax=ax, sheet_name='Sheet1', symbol='-ob', plot_type='log')
    Figure.plot(excel_filename=filename, ax=ax, sheet_name='Sheet2', symbol='-or', plot_type='log', legend=True)
else:
    Config.legend = ['sacrificial material', 'black resin (reference)']
    Config.xlims = {'min': 0, 'max': 1200}
    Config.plot_xlabel = r'set channel width ($\mu$m)'
    Config.plot_ylabel = r'measured channel width ($\mu$m)'
    Figure.plot(excel_filename=filename, ax=ax, sheet_name='py_hp_sm', symbol='-ob')
    Figure.plot(excel_filename=filename, ax=ax, sheet_name='py_hp_br', symbol='-or', legend=True, diagonal=True)
    print("hello, mike")

Figure.save(excel_filename=args.filename, dest=Config.output_dir)