#!/usr/bin/env python3

import os
import sys
import logging
import argparse
import matplotlib.axes
from enum import Enum

import pandas as pd

from src.config import Config
from src.figure import Figure
from src.channel_width import ChannelWidth
from src.widths import Widths

logging.basicConfig(level=logging.INFO, format='%(asctime)s | %(levelname)s | %(message)s')
logger = logging.getLogger(__name__)

"""
ABBREVIATIONS

hp: horizontal print or perpendicular print direction
vp: vertical print or parallel print direction

br: black resin
sm: sacrificial material (AKA wax)

"""

# Global variables:
filename: str = ''


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
    width_diff = 'width_diff'
    width_rel_err = 'width_rel_err'

    def __str__(self):
        return self.value


class Run:
    """Runners for each user selected option"""

    @classmethod
    def plot_channel_widths(cls, before_bake: str, after_bake: str, suffix: str) -> None:
        """Create scatter plots of set and measured width under two conditions."""
        logger.info(f'Making plots of channel width before and after baking')
        logger.info(f'Parameters: {before_bake} and {after_bake}')
        Config.legend = ['before baking', 'after baking']
        Config.xlims = {'min': 0, 'max': 1600}
        Config.plot_xlabel = r'Set channel width ($\mu$m)'
        Config.plot_ylabel = r'Measured channel width ($\mu$m)'
        ax_obj: matplotlib.axes = Figure.plot_conductivity(
            excel_filename=filename, sheet_name=before_bake, symbol='-ob')
        Figure.plot_conductivity(excel_filename=filename, sheet_name=after_bake, ax_obj=ax_obj,
                                 title=Config.plot_title, symbol='-or', legend=True, diagonal=True)
        Figure.save(excel_filename=filename, dest=Config.output_dir, suffix=Widths.specs[suffix]['suffix'])

    @classmethod
    def plot_widths_difference(cls, excel_filename: str, data_frame: pd.DataFrame, specs: dict):
        """Create stem plots of differences recorded under two conditions."""
        experiment_specs = ChannelWidth(dataframe=data_frame, prior=specs['before'], past=specs['after'])
        experiment_specs.get_differences()
        Figure.plot_differences(
            x=experiment_specs.differences['channel_id'].astype("string"),  # casting to string makes x-axis categorical
            y=experiment_specs.differences['width_diff'],
            material=experiment_specs.prior['material'],
            direction=experiment_specs.prior['print_direction'],
        )
        Figure.save(excel_filename=excel_filename, dest=Config.output_dir, suffix=specs['suffix'])


    @classmethod
    def plot_widths_fractional_difference2(cls, excel_filename: str, data_frame: pd.DataFrame, specs: dict):
        """Plots the fraction of channel expansion, so (after - before) / before for each channel ID"""
        channel_width = ChannelWidth(dataframe=data_frame, prior=specs['before'], past=specs['after'])
        channel_width.get_fractional_differences2()
        Figure.plot_widths_fractional_differences(
            x=channel_width.differences['channel_id'].astype("string"),  # casting to string makes x-axis categorical
            y=channel_width.differences['width_frac_diff'],
            yerr=channel_width.differences['width_err'],
            material=channel_width.prior['material'],
            direction=channel_width.prior['print_direction']
        )
        Figure.save(excel_filename=excel_filename, dest=Config.output_dir, suffix=f"{specs['suffix']}_bar")

    @classmethod
    def plot_channel_width_and_difference(cls, excel_filename: str, data_frame_: pd.DataFrame, specs_: dict):
        """Plot channel widths and difference on same graph"""
        channel_width = ChannelWidth(dataframe=data_frame_, prior=specs_['before'], past=specs_['after'])
        channel_width.get_widths()
        channel_width.get_differences()
        Figure.plot_channel_widths_and_differences(
            widths=channel_width.widths,
            diffs=channel_width.differences,
            material=channel_width.prior['material'],
            direction=channel_width.prior['print_direction']
        )

        Figure.save(excel_filename=excel_filename, dest=Config.output_dir, suffix=specs_['suffix'])

    @classmethod
    def plot_width_relative_error(cls, excel_filename: str, data_frame_: pd.DataFrame, specs_: dict) -> None:
        """Plot the relative error for each set channel width"""
        channel_width = ChannelWidth(dataframe=data_frame_, prior=specs_['before'], past=specs_['after'])
        channel_width.get_relative_error()
        Figure.plot_relative_error(
            rel_err=channel_width.relative_error,
            material=channel_width.prior['material'],
            direction=channel_width.prior['print_direction']
        )

        Figure.save(excel_filename=excel_filename, dest=Config.output_dir, suffix=specs_['suffix'])
        pass


def config_channel_study() -> None:
    Config.legend = ['sacrificial material', 'black resin (reference)']
    Config.xlims = {'min': 0, 'max': 1600}
    Config.plot_xlabel = r'set channel width ($\mu$m)'
    Config.plot_ylabel = r'measured channel width ($\mu$m)'


def config_channel_study2() -> None:
    Config.legend = ['before baking', 'after baking']
    Config.xlims = {'min': 0, 'max': 1100}
    Config.ylims = {'min': 0, 'max': 1600}
    Config.plot_xlabel = r'set channel width ($\mu$m)'
    Config.plot_ylabel = r'measured channel width ($\mu$m)'


def config_width_rel_err() -> None:
    Config.legend = ['before baking', 'after baking']
    Config.xlims = {'min': 0, 'max': 1100}
    Config.ylims = {'min': 0, 'max': 300}
    Config.plot_xlabel = r'Set channel width ($\mu$m)'
    Config.plot_ylabel = 'Relative error of measured width (%)'


def main():
    # Set globals:
    global filename

    is_file_save: bool = True

    parser = argparse.ArgumentParser(description="Artificial Muscle Project")
    parser.add_argument('filename', type=str, help='Path to the Excel file')
    parser.add_argument('type', type=Type, choices=list(Type), help='Type of data to plot')
    # parser.add_argument('suffix', type=str, help='Specifies output filename')
    args = parser.parse_args()

    filename = os.path.join(Config.output_dir, args.filename)  # that's global!

    logging.info(f'file name: {filename}')
    logging.info(f'data type to process: {args.type}')

    if args.type == Type.conductivity:
        Config.plot_title = 'Conductivity of carbon mesoporous in TangoPlus'
        # Config.plot_title = 'Conductivity of carbon nanofibers in TangoPlus'
        Config.plot_xlabel = 'fraction CMPs added (weight %)'
        # Config.legend = ['sacrificial material', 'black resin (reference)']
        Figure.plot_conductivity(excel_filename=filename, sheet_name='Sheet1', title=Config.plot_title,
                                 symbol='-ob', y_scale='log')
        # Figure.plot(excel_filename=filename, ax=ax, sheet_name='Sheet2', symbol='-or', plot_type='log', legend=True)
    elif args.type == Type.width:
        is_file_save = False  # with this switch figures are saved with each iteration of for loop
        df = Figure.get_dataframe(excel_filename=filename)
        for key in Widths.specs:
            try:
                Run.plot_widths_fractional_difference2(
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
        Run.plot_channel_widths(before_bake='py_hp_sm_prior', after_bake='py_hp_sm_past', suffix='perp_sm')
        is_file_save = False
    elif args.type == Type.vp_sm:
        Config.plot_title = 'Sacrificial material, parallel to print direction'
        config_channel_study2()
        Run.plot_channel_widths(before_bake='py_vp_sm_prior', after_bake='py_vp_sm_past', suffix='para_sm')
        is_file_save = False
    elif args.type == Type.hp_br:
        Config.plot_title = 'Black resin, perpendicular to print direction'
        config_channel_study2()
        Run.plot_channel_widths(before_bake='py_hp_br_prior', after_bake='py_hp_br_past', suffix='perp_br')
        is_file_save = False
    elif args.type == Type.vp_br:
        Config.plot_title = 'Black resin, parallel to print direction'
        config_channel_study2()
        Run.plot_channel_widths(before_bake='py_vp_br_prior', after_bake='py_vp_br_past', suffix='para_br')
        is_file_save = False

    elif args.type == Type.width_diff:
        is_file_save = False  # with this switch figures are saved with each iteration of for loop
        config_channel_study2()
        df = Figure.get_dataframe(excel_filename=filename)
        for key in Widths.specs:
            try:
                Run.plot_channel_width_and_difference(
                    excel_filename=filename,
                    data_frame_=df,
                    specs_=Widths.specs[key]
                )
            except ValueError:
                logging.error('Config.py_all is either empty or has whitespace - set to existing sheet name')
                sys.exit()

    elif args.type == Type.width_rel_err:
        is_file_save = False
        config_width_rel_err()
        df = Figure.get_dataframe(excel_filename=filename)
        for key in Widths.specs:
            try:
                Run.plot_width_relative_error(
                    excel_filename=filename,
                    data_frame_=df,
                    specs_=Widths.specs[key]
                )
            except ValueError:
                logging.error('Config.py_all is either empty or has whitespace - set to existing sheet name')
                sys.exit()

    if is_file_save:
        Figure.save(excel_filename=args.filename, dest=Config.output_dir, suffix=str(args.type))


if __name__ == '__main__':
    main()
