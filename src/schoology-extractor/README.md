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
only want to list the grading periods for the current school year. Run `poetry
run python grading_periods.py` to get a list of grading periods (requires that
the `.env` file has the key and secret values already configured).

-   `SCHOOLOGY_KEY=<administrator's API key>`
-   `SCHOOLOGY_SECRET=<administrator's API secret>`
-   `SCHOOLOGY_OUTPUT_PATH=<output directory>`
-   `SCHOOLOGY_SECTION_IDS=<csv list of sections' ids>`

## Execution

```bash
poetry install
poetry run python.exe main.py
```

## Test Coverage Report

```bash
poetry run coverage report
```

## Output

Four files in the `./output` directory:

-   `users-<datetimestamp>.csv`
-   `sections-<datetimestamp>.csv`
-   `assignments-<datetimestamp>.csv`
-   `submissions-<datetimestamp>.csv`
