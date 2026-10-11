# Laboratory work
# Made by Stanislav Baleev
# Console Utility Streamstats

## About the project

This project is a command-line utility written in Python
The main function:

* a module that generates reports based on jsonl/csv data

## Requirements

To run this project you need:
* Python 3.10 or higher
* Git
* uv for managing project environment and dependence

## Installation
Download the project and open terminal in its directory

```Bash
git clone https://github.com/Slava-silang/LabworkPython2.git
cd LabworkPython2
```

Then install dependencies and creat project

```Bash
uv sync
```
### Streamstats

The module is started with

```Bash
python -m streamstats analyze <input files> --format <jsonl, csv> 
```

The analysis supports:
* jsonl files
* csv files
### Streamstats also supports arguments:
```Bash
  --output <name of file>
```
* This parameter directs output to specified file
* Without it program run output to stdout

```Bash
--skip-invalid
```

* This parameter lets the module to skip invalid lines and directs warnings to WARNING.log
* Without it program raise error when faces with invalid line
