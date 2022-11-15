import sys
import os
import logging
import argparse
import pandas as pd
import matplotlib.pyplot as plt

logging.basicConfig(level=logging.INFO)

parser = argparse.ArgumentParser(description="Artificial Muscle Project")
parser.add_argument('filename', type=str, help='Path to the Excel file')
args = parser.parse_args()

output_dir = 'C:\\Users\\mkrause.RIZIA-PC\\OneDrive - Naval Postgraduate School\\artificial_muscle\\data'

#print(args)
#
# print(len(sys.argv))
#
# for arg in range(len(sys.argv)):
#     print(f'arg: {sys.argv[arg]}')

# print(f'arg: {sys.argv[1]}')


#filename = os.path.join(output_dir, sys.argv[1])
filename = os.path.join(output_dir, args.filename)
# filename = 'data/data01_cnf.xlsx'
logging.info(f'file name: {filename}')

df = pd.read_excel(filename, sheet_name='Sheet1', index_col=1)
#pd.DataFrame.info(df)
df['y'].plot()

figure_filename = args.filename.split('.')[0] + '.png'
dest = os.path.join(output_dir, figure_filename)
plt.savefig(dest)
if os.path.exists(f'{dest}'):
    logging.info(f'Wrote file {figure_filename} to {dest}')
else:
    logging.warning('Could not write file')
