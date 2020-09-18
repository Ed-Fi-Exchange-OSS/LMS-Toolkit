# Google Classroom Data Extractor

The purpose of this project is to make it easy to extract
Google Classroom data in order to monitor the progress and
participation of students in virtual or blended models.

This data extractor targets two audiences.  The first is
someone who just wants the data out of Google Classroom into a
.csv file that can be loaded into a spreadsheet.  The second
for someone who is familiar with Jupyter Notebook, a common
Python-based tool for analysis and reporting.

## API Permissions

In order to extract data, the Google Classroom APIs must be
enabled, and the application must be granted permission.

A Google Classroom administrator will need to enable both the
Google Classroom API and the Admin SDK.  This can be done
[here](https://console.developers.google.com/apis/library).

Next, the administrator will need to create a Service Account
and API key.  This is the account the application will use for
access.  This can be done
[here](https://console.cloud.google.com/iam-admin/serviceaccounts/create).

 1. Give the new service account a name like "Ed-Fi Extractor"
    and click Create.
 1. Grant the service account the Project Viewer role and click
    Continue then Done.
 1. The new service account will be displayed in a table.
    Click on the three dots for the account and select Create
    Key.
 1. Choose JSON and click Create.
 1. A JSON file will be downloaded from your browser, which is
    the API key.  Rename it to service-account.json.
 1. Finally, click on the service account to view details and
    copy the Unique ID field for the next step.

Finally, the administrator will need to specify the scope of
access for the service account.  This can be done
[here](https://admin.google.com/ac/owl/domainwidedelegation).

1. Add a new API client and provide the service account Unique
   ID in the Client ID field.
1. Paste the following scopes into the OAuth scopes field and
   click Authorize:

`https://www.googleapis.com/auth/admin.directory.orgunit,
https://www.googleapis.com/auth/admin.reports.usage.readonly,
https://www.googleapis.com/auth/classroom.courses,
https://www.googleapis.com/auth/classroom.coursework.students,
https://www.googleapis.com/auth/classroom.profile.emails,
https://www.googleapis.com/auth/classroom.rosters,
https://www.googleapis.com/auth/classroom.student-submissions.students.readonly,
https://www.googleapis.com/auth/admin.reports.audit.readonly`

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
1. Copy the "example.env" file to ".env" and set the variables
   as documented in the file.
1. Place the service-account.json file downloaded earlier in
   the root directory of this project.

## Running the Extractor

### Generate CSV Files

To pull data from Google Classroom and generate csv files, run
`poetry run python google-extractor/main.py` from the root
directory of this project.

### usage.csv

usage.csv is an extract of student usage Google Classroom. Rows
are a pairing of student email and as-of date. The as-of date
applies to the number of posts a student made on that day to
any course. The last interaction time applies to any
interaction the student had with Google Classroom, but does not
provide historical information beyond that.  Last login time is
the last actual login event and does not provide historical
information beyond that either.

### submissions.csv

submission.csv is an extract of student classwork submissions
to Google Classroom. Rows are individual submissions for
assigned coursework per student. Important submission states
include "CREATED", "TURNED_IN" and "RETURNED".  The "CREATED"
state only indicates the assignment of coursework by the
teacher, not student activity.

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

