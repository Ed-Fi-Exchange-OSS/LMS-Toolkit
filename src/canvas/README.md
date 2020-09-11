# Canvas LMS

The purpose of this project is to serve a set of tools to extract data from
Canvas and analyze it.

This data extractor targets two audiences. The first is someone who just wants
the data out of Canvas LMS into a .csv file that can be loaded into a
spreadsheet. The second for someone who is familiar with Jupyter Notebook, a
common Python-based tool for analysis and reporting.

## Folder Structure

You can explore the work done by navigating across the subfolders that you can
see inside the current folder.

## Installing and running the tools

### Requirements

1. Python 3.8
1. Poetry 1.0.10
1. Optional/Recomended: Last version of VSCode

### Installation

Following the next steps, you should be able to execute all the code:

1. Run the command `poetry install` in this folder.
1. Copy the .env.example file to .env and update its values.
1. In vscode type `ctrl`+`shift`+`p` and search for the command `Python: select
   interpreter`, then point it to your generated folder `canvas/.venv`.

### Running the tools

You can run the tools following this steps:

-   For data-extractor:

    -   Run the command `poetry run python.exe ./data-extractor/main.py`

-   For analyze-canvas-data:
    1. Open the `test.ipynb` notebook in VSCode.
    1. Select the generated virtual environment `canvas/.venv` as interpreter in
       the notebook. In VSCode you only have to click the python version in the
       upper right corner, and it should show the option for selecting the
       virtual environment.
    1. When opening the notebook in VSCode, you could see a message asking you
       to install some dependencies, you should install them.
    1. Run the code.
