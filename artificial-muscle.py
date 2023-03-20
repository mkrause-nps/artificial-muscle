#!/usr/bin/env python3

import os
import sys
import logging
import argparse
from enum import Enum

import pandas as pd

from src.config import Config
from src.figure import Figure
from src.channel_width import ChannelWidth
from src.widths import Widths

#logging.basicConfig(level=logging.INFO)
logging.basicConfig(level=logging.INFO, format='%(asctime)s | %(levelname)s | %(message)s')
logger = logging.getLogger(__name__)


"""
ABBREVIATIONS

hp: horizontal print or perpendicular print direction
vp: vertical print or parallel print direction

br: black resin
sm: sacrificial material (AKA wax)

"""


class Type(Enum):
    """User specifies the type of data to be plotted on command line."""
    conductivity = 'conductivity'
    width = 'width'
    hp_sm = 'hp_sm'
    vp_sm = 'vp_sm'
    hp_br = 'hp_br'
    vp_br = 'vp_br'
    hp_prior = 'hp_prior'
    vp_prior = 'vp_prior'
    hp_past = 'hp_past'
    vp_past = 'vp_past'

    def __str__(self):
        return self.value


class Util:

    @classmethod
    def plot_channel_widths(cls, sm_sheet, br_sheet):
        #Config.legend = ['sacrificial material', 'black resin (reference)']
        Config.legend = ['before baking', 'after baking']
        Config.xlims = {'min': 0, 'max': 1600}
        Config.plot_xlabel = r'set channel width ($\mu$m)'
        Config.plot_ylabel = r'measured channel width ($\mu$m)'
        Figure.plot(excel_filename=filename, ax=ax, sheet_name=sm_sheet, symbol='-ob')
        Figure.plot(excel_filename=filename, ax=ax, sheet_name=br_sheet,
                    title=Config.plot_title, symbol='-or', legend=True, diagonal=True)

    @classmethod
    def run_widths_difference(cls, excel_filename: str, data_frame: pd.DataFrame, specs: dict):
        experiment_specs = ChannelWidth(dataframe=data_frame, prior=specs['before'], past=specs['after'])
        experiment_specs.get_differences()
        Figure.plot_differences(
            x=experiment_specs.differences['channel_id'].astype("string"),  # casting to string makes x-axis categorical
            y=experiment_specs.differences['width_diff'],
            material=experiment_specs.prior['material'],
            direction=experiment_specs.prior['print_direction'],
            prior=experiment_specs.prior['status'],
            past=experiment_specs.past['status']
        )
        Figure.save(excel_filename=excel_filename, dest=Config.output_dir, suffix=specs['suffix'])


def config_channel_study():
    Config.legend = ['sacrificial material', 'black resin (reference)']
    Config.xlims = {'min': 0, 'max': 1600}
    Config.plot_xlabel = r'set channel width ($\mu$m)'
    Config.plot_ylabel = r'measured channel width ($\mu$m)'


def config_channel_study2():
    Config.legend = ['before baking', 'after baking']
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
    # Config.plot_title = 'Conductivity of carbon nanofibers in TangoPlus'
    Config.plot_xlabel = 'fraction CMPs added (weight %)'
    # Config.legend = ['sacrificial material', 'black resin (reference)']
    Figure.plot(excel_filename=filename, ax=ax,
                sheet_name='Sheet1', title=Config.plot_title, symbol='-ob', plot_type='log')
    # Figure.plot(excel_filename=filename, ax=ax, sheet_name='Sheet2', symbol='-or', plot_type='log', legend=True)
elif args.type == Type.width:
    df = Figure.get_dataframe(excel_filename=filename)
    for key in Widths.specs:
        try:
            Util.run_widths_difference(
                excel_filename=filename,
                data_frame=df,
                specs=Widths.specs[key]
            )
        except ValueError:
            logging.error('Config.py_all is either empty or has whitespace - set to existing sheet name')
            sys.exit()

elif args.type == Type.hp_sm:
    Config.plot_title = 'Sacrificial material, perpendicular to print direction'
    config_channel_study2()
    Util.plot_channel_widths(sm_sheet='py_hp_sm_prior', br_sheet='py_hp_sm_past')
elif args.type == Type.vp_sm:
    Config.plot_title = 'Sacrificial material, parallel to print direction'
    config_channel_study2()
    Util.plot_channel_widths(sm_sheet='py_vp_sm_prior', br_sheet='py_vp_sm_past')

elif args.type == Type.hp_br:
    Config.plot_title = 'Black resin, perpendicular to print direction'
    config_channel_study2()
    Util.plot_channel_widths(sm_sheet='py_hp_br_prior', br_sheet='py_hp_br_past')
elif args.type == Type.vp_br:
    Config.plot_title = 'Black resin, parallel to print direction'
    config_channel_study2()
    Util.plot_channel_widths(sm_sheet='py_vp_br_prior', br_sheet='py_vp_br_past')


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
