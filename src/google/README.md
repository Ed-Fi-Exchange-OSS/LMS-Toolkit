# Google Classroom Data Extractor

The purpose of this project is to make it easy to extract Google Classroom data in order to monitor the progress and participation of students in virtual or blended models.

This data extractor targets two audiences.  The first is someone who just wants the data out of Google Classroom into a .csv file that can be loaded into a spreadsheet.  The second is to present the data in Jupyter Notebook format for analysis and reporting by someone who is familiar with that common Python-based analytics tool.

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

1. Install the latest version of Python.  You can find it [here](https://www.python.org/downloads/)

1. Clone this GitHub repository and open a command prompt in the root directory of this project (where this file resides).

1. Install pipenv from the command line: `pip install pipenv`

1. Install the third-party libraries used by the extractor: `pipenv install`

1. If you want to do hack the Python code, install the developer tools: `pipenv install --dev`

1. Copy the "example.env" file to ".env" and set the variables as documented in the file.

1. Place the service-account.json file downloaded earlier in the root directory of this project (where this file resides).

## Running the Extractor

1. To pull data from Google Classroom and generate csv files, run `pipenv run python src/main.py` from the root directory of this project.
1. Optional: To open the .ipynb Jupyter Notebook files standalone, run `jupyter notebook`.
1. Optional: To work in Visual Studio, install the Python Extension.  Then type `Ctrl-Shift-P`, select Python:Select Interpreter and choose pipenv for current folder. The
.ipynb Jupiter Notebook files can be opened directly in Visual Studio Code.

