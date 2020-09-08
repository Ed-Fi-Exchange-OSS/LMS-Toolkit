# Zoom data extractor

The purpose of this project is to make it easy to extract
Zoom Meetings data through their APIs.

This data extractor targets two audiences.  The first is
someone who just wants the data out of Zoom Meetings into a
.csv file that can be loaded into a spreadsheet.  The second
for someone who is familiar with Jupyter Notebook, a common
Python-based tool for analysis and reporting.

## Installing the Extractor

1. Install a current version of Python.  The extractor has
   been tested against Python 3.8.5.  You can find it
   [here](https://www.python.org/downloads/).
1. Install Poetry, a Python tool for downloading third-party
   libraries.  You can find installation instructions
   [here](https://python-poetry.org/docs/#installation). The
   instructions are basically a long single-line command to
   copy and run on Powershell (for Windows) or bash (for
   Mac/Linux).
1. Clone this GitHub repository and open a command prompt in
   the root directory of this project (where this README file
   resides).
1. Configure Poetry to put Python enivronments in the right place: `poetry
   config virtualenvs.in-project true`.
1. Install the third-party libraries used by the extractor:
   `poetry install`. This may take a while.

## Authentication

This projectuses a JWT token to authorize the requests
made to the Zoom API.<br>
[JWT with Zoom](https://marketplace.zoom.us/docs/guides/auth/jwt)

## Running the Extractor

### Generate CSV Files

### Analyze with Jupyter Notebook

To open the .ipynb Jupyter Notebook files standalone, run
`jupyter notebook`.  More information about Jupyter Notebooks
in general can be found
[here](https://jupyter-notebook.readthedocs.io/en/stable/notebook.html).

### Visual Studio Code (Optional)

To work in Visual Studio Code install the Python Extension.
Then:
1. Type `Ctrl-Shift-P`, then
   choose `Python:Select Interpreter` and then choose the
   environment that includes `.venv` in the name.
1. .ipynb Jupiter Notebook files can be opened directly in
Visual Studio Code.
