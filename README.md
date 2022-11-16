# Artificial Muscle Data Presentation

Contains a Python 3 script to construct a 
plot of conductivity data.

## Usage
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