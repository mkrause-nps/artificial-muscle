#!/usr/bin/env python3

import os
import logging
import argparse
from src.config import Config
from src.figure import Figure

logging.basicConfig(level=logging.INFO)

parser = argparse.ArgumentParser(description="Artificial Muscle Project")
parser.add_argument('filename', type=str, help='Path to the Excel file')
args = parser.parse_args()

filename = os.path.join(Config.output_dir, args.filename)
logging.info(f'file name: {filename}')

_, ax = Figure.figure_handle()
Figure.plot(excel_filename=filename, ax=ax, sheet_name='Sheet1', symbol='-ob')
Figure.plot(excel_filename=filename, ax=ax, sheet_name='Sheet2', symbol='-or', legend=True)
Figure.save(excel_filename=args.filename, dest=Config.output_dir)
