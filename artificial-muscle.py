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
    conductivity = 'conductivity'
    hp_prior = 'hp_prior'
    vp_prior = 'vp_prior'
    hp_after = 'hp_after'
    vp_after = 'vp_after'

    def __str__(self):
        return self.value


class Util:
    @classmethod
    def plot_channel_widths(cls, sm_sheet, br_sheet):
        Config.legend = ['sacrificial material', 'black resin (reference)']
        Config.xlims = {'min': 0, 'max': 1500}
        Config.plot_xlabel = r'set channel width ($\mu$m)'
        Config.plot_ylabel = r'measured channel width ($\mu$m)'
        Figure.plot(excel_filename=filename, ax=ax, sheet_name=sm_sheet, symbol='-ob')
        Figure.plot(excel_filename=filename, ax=ax, sheet_name=br_sheet,
                    title=Config.plot_title, symbol='-or', legend=True, diagonal=True)


parser = argparse.ArgumentParser(description="Artificial Muscle Project")
parser.add_argument('filename', type=str, help='Path to the Excel file')
parser.add_argument('type', type=Type, choices=list(Type), help='Type of data to plot')
#parser.add_argument('suffix', type=str, help='Specifies output filename')
args = parser.parse_args()

filename = os.path.join(Config.output_dir, args.filename)

logging.info(f'file name: {filename}')
logging.info(f'data type to process: {args.type}')

_, ax = Figure.figure_handle()
if args.type == Type.conductivity:
    Figure.plot(excel_filename=filename, ax=ax, sheet_name='Sheet1', symbol='-ob', plot_type='log')
    Figure.plot(excel_filename=filename, ax=ax, sheet_name='Sheet2', symbol='-or', plot_type='log', legend=True)
elif args.type == Type.hp_prior:
    Config.plot_title = 'Channel printed perpendicular to print direction'
    Config.legend = ['sacrificial material', 'black resin (reference)']
    Config.xlims = {'min': 0, 'max': 1500}
    Config.plot_xlabel = r'set channel width ($\mu$m)'
    Config.plot_ylabel = r'measured channel width ($\mu$m)'
    Util.plot_channel_widths(sm_sheet='py_hp_sm', br_sheet='py_hp_br')
elif args.type == Type.vp_prior:
    Config.plot_title = 'Channel printed parallel to print direction'
    Config.legend = ['sacrificial material', 'black resin (reference)']
    Config.xlims = {'min': 0, 'max': 1500}
    Config.plot_xlabel = r'set channel width ($\mu$m)'
    Config.plot_ylabel = r'measured channel width ($\mu$m)'
    Util.plot_channel_widths(sm_sheet='py_vp_sm', br_sheet='py_vp_br')

Figure.save(excel_filename=args.filename, dest=Config.output_dir, suffix=str(args.type))