# Google Classroom Extractor

This tool retrieves and writes out to CSV students, active sections,
assignments, and submissions by querying the Google Classroom API. For more
information on the this tool and its output files, please see the main
repository [readme](https://github.com/Ed-Fi-Exchange-OSS/LMS-Toolkit).

## Getting Started

1. Download the latest code from [the project
   homepage](https://github.com/Ed-Fi-Exchange-OSS/LMS-Toolkit) by clicking on
   the green "CODE" button and choosing an appropriate option. If choosing the
   Zip option, extract the file contents using your favorite zip tool.
1. Open a command prompt\* and change to this file's directory (\* e.g. cmd.exe,
   PowerShell, bash).
1. Ensure you have [Python 3.9+ and
   Poetry](https://github.com/Ed-Fi-Exchange-OSS/LMS-Toolkit#getting-started).
1. At a command prompt, install all required dependencies:

   ```bash
   poetry install
   ```

1. Optional: make a copy of the `.env.example` file, named simply `.env`, and
   customize the settings as described in the Configuration section below.
1. Place the service-account.json file described below into
   the root directory of this project.
1. Run the extractor one of two ways:
   * Execute the extractor with minimum command line arguments:

      ```bash
      poetry run python edfi_google_classroom_extractor -a [admin account email]
      ```

   * Alternately, run with environment variables or `.env` file:

     ```bash
     poetry run python edfi_google_classroom_extractor
     ```

   * For detailed help, execute `poetry run python canvas_extractor -h`.

## Configuration

### Configuration

Application configuration is provided through environment variables or command
line interface (CLI) arguments. CLI arguments take precedence over environment
variables. Environment variables can be set the normal way, or by using a
dedicated [`.env` file](https://pypi.org/project/python-dotenv/) like:

```none
CLASSROOM_ACCOUNT[<email address of the Google Classroom admin account, required]
LOG_LEVEL=[Log level, optional]
OUTPUT_PATH=[The output directory for the csv files, optional]
START_DATE=[start date for usage data pull in yyyy-mm-dd format, optional]
END_DATE=[end date for usage data pull in yyyy-mm-dd format, optional]
```

Supported parameters:

| Description | Required | Command Line Argument | Environment Variable |
| ----------- | -------- | --------------------- | -------------------- |
| The email address of the Google Classroom admin account. | yes | `-a` or `--classroom-account` | CLASSROOM_ACCOUNT |
| The log level for the tool. | no (default: INFO) | `-l` or `--log-level` | LOG_LEVEL |
| The output directory for the generated csv files. | no (default: data/) | `-s` or `--usage-start-date` | OUTPUT_PATH |
| Start date*, yyyy-mm-dd format | no (default: today) | `-s` or `--usage-start-date` | START_DATE |
| End date*, yyyy-mm-dd format | no (default: today) | `-e` or `--usage-end-date` | END_DATE |
| Number of retry attempts for failed API calls | no (default: 4) | none | REQUEST_RETRY_COUNT |
| Timeout window for retry attempts, in seconds | no (default: 60 seconds) | none | REQUEST_RETRY_TIMEOUT_SECONDS |

\* _Start Date_ and _End Date_ are used in pulling system activity (usage)
data and could span any relevant date range.

\** Valid values for the optional _log level_:

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
1. Grant the service account the "Viewer" role and click `Continue` then
   Done, skipping step 3: "Grant users access to this service account".
1. The new service account will be displayed in a table.
   Click on the three dots for the account and select Manage Keys.
1. On the next page, click the `Add Key` button, then choose JSON and click
   `Create` in the dialog box.
1. A JSON file will be downloaded from your browser, which is the API key.
   Rename it to `service-account.json`. Save this into the project directory.
1. Finally, click on the service account to view details and
   copy the Unique ID field for the next step.

Finally, the administrator will need to specify the scope of
access for the service account.  This can be done
[here](https://admin.google.com/ac/owl/domainwidedelegation).

1. Add a new API client and provide the service account Unique
   ID (`client_id` in the json file) in the `Client ID` field.
1. Paste the following scopes into the OAuth scopes field and
   click `Authorize`:

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
`poetry run python edfi_google_classroom_extractor` from the root
directory of this project. CSV files are output into the
`data/ed-fi-udm-lms` directory.

### TLS/SSL proxying

Users on a corporate network that intercepts TLS/SSL traffic will need to have a
copy of the corporate root certificate on file, and then add an environment
variable pointing to this file: `HTTPLIB2_CA_CERTS=[absolute path to
certificate]`. NOTE: this does not load properly through the `.env` file, and
must be set as an actual environment variable.

### Logging and Exit Codes

Log statements are written to the standard output. If you wish to capture log
details, then be sure to redirect the output to a file. For example:

```bash
poetry run python google_classroom_extractor > 2020-12-07-15-43.log
```

If any errors occurred during the script run, then there will be a final print
message to the standard error handler as an additional mechanism for calling
attention to the error: `"A fatal error occurred, please review the log output
for more information."`

The application will exit with status code `1` if there were any log messages at
the ERROR or CRITICAL level, otherwise it will exit with status code `0`.

## Developer Operations

1. Style check: `poetry run flake8`
1. Static typing check: `poetry run mypy .`
1. Run unit tests: `poetry run pytest`
1. Run unit tests with code coverage: `poetry run coverage run -m pytest`
1. View code coverage: `poetry run coverage report`

_Also see
[build.py](https://github.com/Ed-Fi-Exchange-OSS/LMS-Toolkit/blob/main/docs/build.md)_
for use of the build script.

### Visual Studio Code (Optional)

To work in Visual Studio Code install the Python Extension.
Then type `Ctrl-Shift-P`, then choose `Python:Select Interpreter`,
then choose the environment that includes `.venv` in the name.

## Legal Information

Copyright (c) 2021 Ed-Fi Alliance, LLC and contributors.

Licensed under the [Apache License, Version
2.0](https://github.com/Ed-Fi-Exchange-OSS/LMS-Toolkit/blob/main/LICENSE) (the
"License").

Unless required by applicable law or agreed to in writing, software distributed
under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR
CONDITIONS OF ANY KIND, either express or implied. See the License for the
specific language governing permissions and limitations under the License.

See
[NOTICES](https://github.com/Ed-Fi-Exchange-OSS/LMS-Toolkit/blob/main/NOTICES.md)
for additional copyright and license notifications.
