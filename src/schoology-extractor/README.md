# Schoology Extractor

This script retrieves and writes out to CSV all students, sections, assignments,
and submissions for the desired grading period(s).

## Requirements

Requires Python 3.8 and [Poetry](https://python-poetry.org/). To get started,
run the following command in the package directory:

```bash
poetry install
```

## Configuration

Application configuration is provided through environment variables or command
line interface (CLI) arguments. CLI arguments take precedence over environment
variables. Environment variables can be set the normal way, or by using a
dedicated [`.env` file](https://pypi.org/project/python-dotenv/). For `.env`
support, we provided a [.env.example](.env.example) which you can copy, rename
to `.env`, and adjust to your desired parameters. Supported parameters:

| Description | Required | Command Line Argument | Environment Variable |
| ----------- | -------- | --------------------- | -------------------- |
| Schoology API Key | yes | -k or --client-key | SCHOOLOGY_KEY |
| Schoology API Secret | yes |  -s or --client-secret | SCHOOLOGY_SECRET |
| List of Grading Periods | yes | -g or --grading-periods | SCHOOLOGY_GRADING_PERIODS |
| Output Directory | no (default: working directory) | -o or --output-directory | SCHOOLOGY_OUTPUT_PATH |
| Log level | no (default: WARNING) | -l or --log-level | SCHOOLOGY_LOG_LEVEL |
| Page size | no (default: 20) | -p or --page-size | PAGE_SIZE |
| Number of retry attempts for failed API calls | no (default: 4) | none | REQUEST_RETRY_COUNT |
| Timeout window for retry attempts, in seconds | no (default: 60 seconds) | none | REQUEST_RETRY_TIMEOUT_SECONDS |

User's API key and secret are managed at
[https://app.schoology.com/api](https://app.schoology.com/api).

The grading periods list helps determine which grading periods are of interest.
The value should be a comma-separated list of Grading Period Id values, e.g `-g
12345,67899`. For example, an organization with multiple school years in one
Schoology account would only want to list the grading periods for the current
school year.

## Execution

Execute the extractor with CLI args:

```bash
poetry run python.exe schoology_extractor/main.py -k your-schoology-client-key -s your-schoology-client-secret  -g csv-of-grading-periods
```

For detailed help, execute `poetry run python schoology_extractor/main.py -h`.
Alternately, run with environment variables or `.env` file:

```bash
poetry run python.exe schoology_extractor/main.py
```

### Grading Periods Helper

To get a list of all available grading periods, run:

```bash
poetry run python schoology_extractor/grading_periods.py -k your-schoology-client-key -s your-schoology-client-secret
```

As with the main script, you can also use environment variables or a `.env` file in place of the `-k` and `-s` arguments. For detailed help, run:

```bash
poetry run python schoology_extractor/grading_periods.py -h
```

## Output

Four files in the project(or the specified output) directory:

* `users.csv`
* `sections.csv`
* `assignments.csv`
* `submissions.csv`

## Developer Utilities

Unit test execution:

```bash
poetry run pytest
```

Code coverage:

```bash
poetry run coverage run -m pytest
poetry run coverage report
```

Linting:

```bash
poetry run flake8
```

Static type checks:

```bash
poetry run mypy schoology_extractor
```

## Legal Information

Copyright (c) 2020 Ed-Fi Alliance, LLC and contributors.

Licensed under the [Apache License, Version 2.0](LICENSE) (the "License").

Unless required by applicable law or agreed to in writing, software distributed
under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR
CONDITIONS OF ANY KIND, either express or implied. See the License for the
specific language governing permissions and limitations under the License.

See [NOTICES](NOTICES.md) for additional copyright and license notifications.
