# Canvas Extractor

This tool retrieves and writes out to CSV students, active sections,
assignments, and submissions by querying the Canvas API. For more information on
the this tool and its output files, please see the main repository
[readme](https://github.com/Ed-Fi-Exchange-OSS/LMS-Toolkit).

## Getting Started

1. Download the latest code from [the project
   homepage](https://github.com/Ed-Fi-Exchange-OSS/LMS-Toolkit) by clicking on
   the green "CODE" button and choosing an appropriate option. If choosing the
   Zip option, extract the file contents using your favorite zip tool.
1. Open a command prompt\* and change to this file's directory (* e.g. cmd.exe,
   PowerShell, bash).
1. Ensure you have [Python 3.9+ and Poetry](https://github.com/Ed-Fi-Exchange-OSS/LMS-Toolkit#getting-started).
1. At a command prompt, install all required dependencies:

   ```bash
   poetry install
   ```

1. Optional: make a copy of the `.env.example` file, named simply `.env`, and
   customize the settings as described in the Configuration section below.
1. Create an access token by signing into your Canvas instance. Go to Account >
   Settings, then scroll down to the "Approved Integrations" section and click
   the "New Access Token" button. If using a `.env` file, then copy the token
   into this file.
1. Run the extractor one of two ways:
   * Execute the extractor with minimum command line arguments:

      ```bash
      poetry run python edfi_canvas_extractor -b [canvas url] -a [api token]
          -s [start date range] -e [end date range] -f assignments
      ```

   * Alternately, run with environment variables or `.env` file:

     ```bash
     poetry run python edfi_canvas_extractor
     ```

   * For detailed help, execute `poetry run python edfi_canvas_extractor -h`.

## Configuration

Application configuration is provided through environment variables or command
line interface (CLI) arguments. CLI arguments take precedence over environment
variables. Environment variables can be set the normal way, or by using a
dedicated [`.env` file](https://pypi.org/project/python-dotenv/) like

```none
CANVAS_BASE_URL=[CANVAS_BASE_URL]
CANVAS_ACCESS_TOKEN=[CANVAS_ACCESS_TOKEN]
START_DATE=[CLASS_START_DATE]
END_DATE=[CLASS_END_DATE]
OUTPUT_DIRECTORY=data
```

Supported parameters:

| Description | Required | Command Line Argument | Environment Variable |
| ----------- | -------- | --------------------- | -------------------- |
| Base Canvas URL | yes | `-b` or `--base-url` | CANVAS_BASE_URL |
| Canvas API access token | yes | `-a` or `--access-token` | CANVAS_ACCESS_TOKEN |
| Output Directory | no (default: [working directory]/data) | `-o` or `--output-directory` | OUTPUT_DIRECTORY |
| Sync database directory | no (default: [working directory]/data) | `-d` or `--sync-database-directory` | SYNC_DATABASE_DIRECTORY |
| Start date*, yyyy-mm-dd format | yes | `-s` or `--start_date` | START_DATE |
| End date*, yyyy-mm-dd format | yes | `-e` or `--end_date` | END_DATE |
| Log level** | no (default: INFO) | `-l` or `--log-level` | LOG_LEVEL |
| Feature*** | no (default: core, not removable) | `-f` or `--feature` | FEATURE |

\* _Start Date_ and _End Date_ are used in pulling course data and would
typically span a semester or equivalent school calendar timespan.

\** Valid values for the optional _log level_:

* DEBUG
* INFO(default)
* WARNING
* ERROR
* CRITICAL

\*** When there's no specified feature, the extractor will always process Users,
Sections, and Section Associations, which are considered the core feature. Other
features (can combine two or more):

* assignments (Enables the extraction of assignments and submissions)
* grades (Enables the extraction of grades) - **EXPERIMENTAL**, subject to
  breaking changes

When setting features via `.env` file or through environment variable, combine
features by using a bracketed comma-separate list, e.g. `FEATURE=[assignments,
grades]`. To combine features at the command line, simply list them together:
`--feature assignments, grades`.

### Output

CSV files in the data(or the specified output) directory with the [LMS Unifying
Data
Model](https://techdocs.ed-fi.org/display/EDFITOOLS/LMS+Unifying+Data+Model)
format.

### Logging and Exit Codes

Log statements are written to the standard output. If you wish to capture log
details, then be sure to redirect the output to a file. For example:

```bash
poetry run python edfi_canvas_extractor > 2020-12-07-15-43.log
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
[build.py](https://github.com/Ed-Fi-Exchange-OSS/LMS-Toolkit/blob/main/docs/build.md)_ for
use of the build script.

### Visual Studio Code (Optional)

To work in Visual Studio Code install the Python Extension.
Then type `Ctrl-Shift-P`, then choose `Python:Select Interpreter`,
then choose the environment that includes `.venv` in the name.

## Legal Information

Copyright (c) 2022 Ed-Fi Alliance, LLC and contributors.

Licensed under the [Apache License, Version
2.0](https://github.com/Ed-Fi-Exchange-OSS/LMS-Toolkit/blob/main/LICENSE) (the
"License").

Unless required by applicable law or agreed to in writing, software distributed
under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR
CONDITIONS OF ANY KIND, either express or implied. See the License for the
specific language governing permissions and limitations under the License.

See [NOTICES](https://github.com/Ed-Fi-Exchange-OSS/LMS-Toolkit/blob/main/NOTICES.md) for
additional copyright and license notifications.
