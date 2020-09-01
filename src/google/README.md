# Google Classroom Data Extractor

The purpose of this project is to make it easy to extract Google Classroom data in order to monitor the progress and participation of students in virtual or blended models.

This data extractor targets two audiences.  The first is someone who just wants the data out of Google Classroom into a .csv file that can be loaded into a spreadsheet.  The second for someone who is familiar with Jupyter Notebook, a common Python-based tool for analysis and reporting.

## API Permissions

In order to extract data, the Google Classroom APIs must be enabled, and the application must be granted permission.

A Google Classroom administrator will need to enable both the Google Classroom API and the Admin SDK.  This can be done [here](https://console.developers.google.com/apis/library).

Next, the administrator will need to create a Service Account and API key.  This is the account the application will use for access.  This can be done [here](https://console.cloud.google.com/iam-admin/serviceaccounts/create).

 1. Give the new service account a name like "Ed-Fi Extractor" and click Create.
 1. Grant the service account the Project Viewer role and click Continue then Done.
 1. The new service account will be displayed in a table.  Click on the three dots for the account and select Create Key.
 1. Choose JSON and click Create.
 1. A JSON file will be downloaded from your browser, which is the API key.  Rename it to service-account.json.
 1. Finally, click on the service account to view details and copy the Unique ID field for the next step.

Finally, the administrator will need to specify the scope of access for the service account.  This can be done [here](https://admin.google.com/ac/owl/domainwidedelegation).

1. Add a new API client and provide the service account Unique ID in the Client ID field.
1. Paste the following scopes into the OAuth scopes field and click Authorize:

`https://www.googleapis.com/auth/admin.directory.orgunit,
https://www.googleapis.com/auth/admin.reports.usage.readonly,
https://www.googleapis.com/auth/classroom.courses,
https://www.googleapis.com/auth/classroom.coursework.students,
https://www.googleapis.com/auth/classroom.profile.emails,
https://www.googleapis.com/auth/classroom.rosters,
https://www.googleapis.com/auth/classroom.student-submissions.students.readonly,
https://www.googleapis.com/auth/admin.reports.audit.readonly`

## Installing the Extractor

1. Install the latest version of Python.  You can find it [here](https://www.python.org/downloads/).

1. Install Poetry, a Python tool for downloading third-party libraries.  You can find installation instructions [here](https://python-poetry.org/docs/#installation). The instructions are basically a long single-line command to copy and run on Powershell (for Windows) or bash (for Mac/Linux).
1. Clone this GitHub repository and open a command prompt in the root directory of this project (where this README file resides).

1. Install the third-party libraries used by the extractor: `poetry install`. This may take a while.

1. Copy the "example.env" file to ".env" and set the variables as documented in the file.

1. Place the service-account.json file downloaded earlier in the root directory of this project.

## Running the Extractor

### Generate CSV Files

To pull data from Google Classroom and generate csv files, run `poetry run python google-extractor/main.py` from the root directory of this project.

### Analyze with Jupyter Notebook

To open the .ipynb Jupyter Notebook files standalone, run `jupyter notebook`.  More information about Jupyter Notebooks in general can be found [here](https://jupyter-notebook.readthedocs.io/en/stable/notebook.html).

### Visual Studio Code (Optional)
To work in Visual Studio Code install the Python Extension.  Then:
1. Close Visual Studio Code and open a new command prompt in the root directory of this project.
1. Run `poetry shell` followed by `vscode .` (Don't forget the period!  Note you will only need run Visual Studio Code like this once.)
1. Visual Studio Code will open. Type `Ctrl-Shift-P`, then choose `Python:Select Interpreter` and then choose the environment that includes `google-extractor` in the name.

The .ipynb Jupiter Notebook files can be opened directly in Visual Studio Code.

