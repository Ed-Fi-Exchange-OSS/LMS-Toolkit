# Google Classroom Extractor

The purpose of this project is to make it easy to extract
Google Classroom data in order to monitor the progress and
participation of students in virtual or blended models.

This data extractor targets two audiences.  The first is
someone who just wants the data out of Google Classroom into a
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
1. Copy the "example.env" file to ".env" in the same directory
   and set the variables as documented in the file.
1. Place the service-account.json file downloaded earlier in
   the root directory of this project.

## Running the Extractor

### Configuration

Application configuration is provided through environment variables or command
line interface (CLI) arguments. CLI arguments take precedence over environment
variables. Environment variables can be set the normal way, or by using a
dedicated [`.env` file](https://pypi.org/project/python-dotenv/). For `.env`
support, we provided a [.env.example](.env.example) which you can copy, rename
to `.env`, and adjust to your desired parameters. Supported parameters:

| Description | Required | Command Line Argument | Environment Variable |
| ----------- | -------- | --------------------- | -------------------- |
| The email address of the Google Classroom admin account. | yes | -a or --classroom-account | CLASSROOM_ACCOUNT |
| The log level for the tool. | no (default: INFO) | -l or --log-level | LOG_LEVEL |
| The output directory for the generated csv files. | no (default: data/) | -s or --usage-start-date | OUTPUT_PATH |
| Start date for usage data pull in yyyy-mm-dd format. | no (default: today) | -s or --usage-start-date | START_DATE |
| End date for usage data pull in yyyy-mm-dd format. | no (default: today) | -e or --usage-end-date | END_DATE |
| Number of retry attempts for failed API calls | no (default: 4) | none | REQUEST_RETRY_COUNT |
| Timeout window for retry attempts, in seconds | no (default: 60 seconds) | none | REQUEST_RETRY_TIMEOUT_SECONDS |

Valid log levels:
* DEBUG
* INFO(default)
* WARNING
* ERROR
* CRITICAL

Note: in order to make the extractor work, you still need to configure your
`service-account.json` file. To do so, read the next section `API Permissions`
### API Permissions

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

### Generate LMS UDM CSV Files

To pull data from Google Classroom and generate csv files, run
`poetry run python google_classroom_extractor` from the root
directory of this project. CSV files are output into the
`data/ed-fi-udm-lms` directory.

### TLS/SSL proxying

Users on a corporate network that intercepts TLS/SSL traffic will need
to have a copy of the corporate root certificate on file, and then add
an environment variable pointing to this file:
`HTTPLIB2_CA_CERTS=<absolute path to certificate>`

### Logging and Exit Codes

Log statements are written to the standard output. If you wish to capture log
details, then be sure to redirect the output to a file. For example:

```bash
poetry run python.exe google_classroom_extractor/main.py > 2020-12-07-15-43.log
```

If any errors occurred during the script run, then there will be a final print
message to the standard error handler as an additional mechanism for calling
attention to the error: `"A fatal error occurred, please review the log output
for more information."`

The application will exit with status code `1` if there were any log messages at
the ERROR or CRITICAL level, otherwise it will exit with status code `0`.

## Dev Operations

1. Style check: `poetry run flake8`
1. Static typing check: `poetry run mypy .`
1. Run unit tests: `poetry run pytest`
1. Run unit tests with code coverage: `poetry run coverage run -m pytest`
1. View code coverage: `poetry run coverage report`


### Visual Studio Code (Optional)

To work in Visual Studio Code install the Python Extension.
Then type `Ctrl-Shift-P`, then choose `Python:Select Interpreter`,
then choose the environment that includes `.venv` in the name.