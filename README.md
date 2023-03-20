# Artificial Muscle Data Presentation

For any Python script to run install requirements (e.g., by using a virtual environment). Run 

`python -m artificial-muscle -h`

to find out input requirements to run the different studies.

## Conductivity Study
A Python 3 script to construct a plot of conductivity data. The conductivity study focuses on answering the question of
how does adding a conductive material to the resin affect the cured resin's conductivity.

### Usage
To run the Python script install requirements (e.g., by using a virtual environment). Then in the project directory execute

`python ./main.py datafilename`

where `datafilename` is the absolute path to 
an Excel file, e.g., `C:\data.xlsx`.

The Excel file needs to contain at least one 
_sheet_ with the following columns:

| Position | Column Header | Datatype | Meaning                                                       |
|----------|---------------|----------|---------------------------------------------------------------|
| 1        | label         | str      | Describes percentage of substance mixed to resin              |
| 2        | x             | float    | X-values                                                      |
| 3        | filtered      | bool     | Is the mixture filtered or not                                |
| 4        | y             | float    | Y-values                                                      |
| 5        | err           | float    | The error (e.g., standard error of the mean) for each Y-value |
| 6        | n             | integer  | The number of samples of Y for a given X                      |

Meta data for a given spreadsheet are specified in 
`config.py`. Change it accordingly.

The output is a semi-logarithmic plot of conductivity
values, which is saved in PNG format to 
the same directory the spreadsheet was loaded from.

## Channel Width Study
The channel width study compares how different orientations of printing the channels affects channel widths. Specifically,
how does printing the channel parallel or perpendicular to the print direction affect the channel width before and
after baking.

The code requires passing an Excel file that contains a tab with the following filenames:
 * py_hp_sm_prior
 * py_vp_sm_prior
 * py_hp_sm_past
 * py_vp_sm_past
 * py_hp_br_prior
 * py_vp_br_prior
 * py_hp_br_past
 * py_vp_br_past

where hp denotes perpendicular and vp parallel print direction, respectively; sm denotes sacrificial material, br denotes
black resin, and prior and past denote whether the specimen has been baked or not.

The tabs need to be of the following format:

| Position | Column Header | Datatype | Meaning                                                       |
|----------|---------------|----------|---------------------------------------------------------------|
| 1        | label         | str      | An Enum: sacrificial material or black resin                  |
| 2        | x             | int      | X-values                                                      |
| 3        | y             | float    | Y-values                                                      |
| 4        | err           | float    | The error (e.g., standard error of the mean) for each Y-value |

Executing the code generates four different kinds of scatter plots, depending on the type parameter.

| Type Parameter | Plot Content                                                                            |
|----------------|-----------------------------------------------------------------------------------------|
| hp_sm          | Channels containing sacrificial material, printed perpendicular before and after baking |
| vp_sm          | Channels containing sacrificial material, printed parallel before and after baking      |
| hp_br          | Channels containing black resin material, printed perpendicular before and after baking |
| vp_br          | Channels containing black resin material, printed parallel before and after baking      |

In the root directory execute

`python -m artificial-muscle <path-to-Excel-datafile> <Type Parameter>`

Files containing the plots are written to the same directory where the Excel datafile resides.

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


