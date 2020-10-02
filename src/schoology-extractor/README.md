# Schoology Assignment Data

This script retrieves and writes out to CSV all students, sections, assignments,
and submissions for the desired grading period(s).

## Requirements

-   Python 3.8.x
-   Poetry

## Configuration

Configuration is via `.env` file or directly with environment variables listed
below. User's API key and secret are managed at https://app.schoology.com/api.
The grading periods list helps determine which grading periods are of interest -
for example, an organization with school years in one Schoology account would
only want to list the grading periods for the current school year. Run `poetry run python grading_periods.py` to get a list of grading periods (requires that
the `.env` file has the key and secret values already configured).

-   `SCHOOLOGY_KEY=<administrator's API key>`
-   `SCHOOLOGY_SECRET=<administrator's API secret>`
-   `SCHOOLOGY_OUTPUT_PATH=<output directory>`
-   `SCHOOLOGY_SECTION_IDS=<csv list of sections' ids>`

(!) Note for MSDF/Ed-Fi users: if you have setup environment variable
`REQUESTS_CA_BUNDLE` to support poetry installs, you actually need to disable it
before running this program. You can do this by setting `REQUESTS_CA_BUNDLE=`
(nothing) in your `.env` file.

## Execution

```bash
poetry install
poetry run python.exe schoology_extractor/main.py
```

## Test Coverage Report

```bash
poetry run coverage run -m pytest

poetry run coverage report
```

## Output

Four files in the `./output` directory:

-   `users.csv`
-   `sections.csv`
-   `assignments.csv`
-   `submissions.csv`
