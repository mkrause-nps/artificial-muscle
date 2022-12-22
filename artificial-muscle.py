#!/usr/bin/env python3

import os
import logging
import argparse
import sys
from enum import Enum
from src.config import Config
from src.figure import Figure
from src.experiment_specs import ExperimentSpecs

logging.basicConfig(level=logging.INFO)


class Type(Enum):
    """User specifies the type of data to be plotted on command line."""
    conductivity = 'conductivity'
    width = 'width'
    hp_prior = 'hp_prior'
    vp_prior = 'vp_prior'
    hp_past = 'hp_past'
    vp_past = 'vp_past'

    def __str__(self):
        return self.value


class Util:

    @classmethod
    def plot_channel_widths(cls, sm_sheet, br_sheet):
        Config.legend = ['sacrificial material', 'black resin (reference)']
        Config.xlims = {'min': 0, 'max': 1600}
        Config.plot_xlabel = r'set channel width ($\mu$m)'
        Config.plot_ylabel = r'measured channel width ($\mu$m)'
        Figure.plot(excel_filename=filename, ax=ax, sheet_name=sm_sheet, symbol='-ob')
        Figure.plot(excel_filename=filename, ax=ax, sheet_name=br_sheet,
                    title=Config.plot_title, symbol='-or', legend=True, diagonal=True)

    @classmethod
    def plot_channel_widths(cls, excel_filename: str):
        specs1 = {
            'status': 'prior',
            'material': 'sacrificial_material',
            'print_direction': 'perpendicular'
        }

        specs2 = {
            'status': 'past',
            'material': 'sacrificial_material',
            'print_direction': 'perpendicular'
        }

        df = Figure.get_dataframe(excel_filename=excel_filename)
        experiment_specs = ExperimentSpecs(dataframe=df, prior=specs1, past=specs2)
        experiment_specs.get_differences()
        experiment_specs.plot_differences()

def config_channel_study():
    Config.legend = ['sacrificial material', 'black resin (reference)']
    Config.xlims = {'min': 0, 'max': 1600}
    Config.plot_xlabel = r'set channel width ($\mu$m)'
    Config.plot_ylabel = r'measured channel width ($\mu$m)'


parser = argparse.ArgumentParser(description="Artificial Muscle Project")
parser.add_argument('filename', type=str, help='Path to the Excel file')
parser.add_argument('type', type=Type, choices=list(Type), help='Type of data to plot')
# parser.add_argument('suffix', type=str, help='Specifies output filename')
args = parser.parse_args()

filename: str = os.path.join(Config.output_dir, args.filename)

logging.info(f'file name: {filename}')
logging.info(f'data type to process: {args.type}')

_, ax = Figure.get_figure_handle()
if args.type == Type.conductivity:
    Config.plot_title = 'Conductivity of carbon mesoporous in TangoPlus'
    Config.plot_xlabel = 'fraction CMP added (weight %)'
    # Config.legend = ['sacrificial material', 'black resin (reference)']
    Figure.plot(excel_filename=filename, ax=ax,
                sheet_name='Sheet1', title=Config.plot_title, symbol='-ob', plot_type='log', legend=False)
    # Figure.plot(excel_filename=filename, ax=ax, sheet_name='Sheet2', symbol='-or', plot_type='log', legend=True)
elif args.type == Type.width:
    #try:
    Util.plot_channel_widths(excel_filename=filename)
    # except ValueError:
    #     logging.error('Config.py_all is either empty or has whitespace - set to existing sheet name')
    #     sys.exit()
elif args.type == Type.hp_prior:
    Config.plot_title = 'Channels perpendicular to print direction - before baking'
    config_channel_study()
    Util.plot_channel_widths(sm_sheet='py_hp_sm_prior', br_sheet='py_hp_br_prior')
elif args.type == Type.vp_prior:
    config_channel_study()
    Config.plot_title = 'Channels parallel to print direction - before baking'
    Util.plot_channel_widths(sm_sheet='py_vp_sm_prior', br_sheet='py_vp_br_prior')
elif args.type == Type.hp_past:
    config_channel_study()
    Config.plot_title = 'Channels perpendicular to print direction - after baking'
    Util.plot_channel_widths(sm_sheet='py_hp_sm_past', br_sheet='py_hp_br_past')
elif args.type == Type.vp_past:
    config_channel_study()
    Config.plot_title = 'Channels parallel to print direction - after baking'
    Util.plot_channel_widths(sm_sheet='py_vp_sm_past', br_sheet='py_vp_br_past')

Figure.save(excel_filename=args.filename, dest=Config.output_dir, suffix=str(args.type))
