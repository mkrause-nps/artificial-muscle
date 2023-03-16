# Artificial Muscle Data Presentation

For any Python script to run install requirements (e.g., by using a virtual environment).

## Conductivity Study
A Python 3 script to construct a plot of conductivity data.

### Usage
To run the Python script install requirements (e.g., by 
using a virtual environment). Then in the project 
direcory execute

`python ./main.py datafilename`

where `datafilename` is the absolute path to 
an Excel file, e.g., `C:\data.xlsx`.

The Excel file needs to contain at least one 
_sheet_ with the following columns:

| Position | Column Header | Datatype | Meaning                                          |
| ------- | ------------- | -------- |--------------------------------------------------|
| 1 | label | str | Describes percentage of substance mixed to resin |
| 2 | x | float | X-values |
| 3 | filtered | bool | Is the mixture filtered or not |
| 4 | y | float | Y-values |
| 5 | err | float | The error (e.g., standard error of the mean) for each Y-value |
| 6 | n | integer | The number of samples of Y for a given X |

Meta data for a given spreadsheet are specified in 
`config.py`. Change it accordingly.

The output is a semi-logarthmic plot of conductivity
values, which is saved in PNG format to 
the same directory the spreadsheet was loaded from.

## Clearance Study

Two scripts can be run within the Clearance Study:
1. **Clearance Length**: A script to analyze and plot the fraction of channel lengths that could be cleared for a given channel size. It writes the plot to disk in PNG format.
2. **Clearance Width**: A script to analyze and write summary plots and CSV files to disk about the widths of the cleared channel. 

### Clearance Length

Specify data directory and filenames at the beginning of the script. Those are used for in- and output of data. Then navigate to `src` and run `python -m clearance_plot`. It generates a PNG file with the data in variable `datafile` in the directory `data_dir` and with filename `figname`.

### Clearance Width

Data for that script are expected in JSON format. To get the data into JSON I copied each of the four the raw data with headers (i.e., for each channel size) into an empty text file, and used a [CSV-to-JSON](https://csvjson.com/csv2json) converter to construct the JSON.

Set values for `data_dir`, `datafile`, `figname` and `labels` in the top of the script and execute `python -m clearance_widths`.

That writes two spreadsheet summary files and two PNG figures into `data_dir`.


