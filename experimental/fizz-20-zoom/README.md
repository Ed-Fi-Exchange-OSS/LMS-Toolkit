# Zoom data extractor

The purpose of this project is to make it easy to extract
Zoom Meetings data through their APIs.

## Installing the Extractor

1. Install a current version of Python. The extractor has
   been tested against Python 3.8.5. You can find it
   [here](https://www.python.org/downloads/).
2. Install Poetry, a Python tool for downloading third-party
   libraries. You can find installation instructions
   [here](https://python-poetry.org/docs/#installation). The
   instructions are basically a long single-line command to
   copy and run on Powershell (for Windows) or bash (for
   Mac/Linux).
3. Clone this GitHub repository and open a command prompt in
   the root directory of this project (where this README file
   resides).
4. Configure Poetry to put Python enivronments in the right place: `poetry config virtualenvs.in-project true`.
5. Install the third-party libraries used by the extractor:
   `poetry install`. This may take a while.

## Authentication

This projectuses a JWT token to authorize the requests
made to the Zoom API.<br>
[JWT with Zoom](https://marketplace.zoom.us/docs/guides/auth/jwt)

## Running the Extractor

To execute the script on windows, run `poetry run python.exe zoom-extractor/main.py`
from the root directory of this Zoom project.

### Visual Studio Code (Optional)

To work in Visual Studio Code install the Python Extension.
Then:

1. Type `Ctrl-Shift-P`, then
   choose `Python:Select Interpreter` and then choose the
   environment that includes `.venv` in the name.
1. .ipynb Jupiter Notebook files can be opened directly in
   Visual Studio Code.

## API Limitations

### Maximum number of requests

Zoom has some restrictions on the number of requests that you can do to their endpoints in a short period of time, each endpoint has its own number of requests allowed depending on your account type(the Plan that you have).
You can find more information about this limitation [here](https://marketplace.zoom.us/docs/api-reference/rate-limits).
