# Schoology Assignment Data

This script retrieves and writes out to CSV all students, sections, assignments,
and submissions for the desired grading period(s).

## Requirements

-   Python 3.8.x
-   Poetry

## Configuration

User's API key and secret are managed at https://app.schoology.com/api.
The grading periods list helps determine which grading periods are of interest -
for example, an organization with school years in one Schoology account would
only want to list the grading periods for the current school year.
Run

```bash
poetry run python schoology_extractor/grading_periods.py -k your-schoology-client-key -s your-schoology-client-secret
```

to get a list of grading periods.

## Execution

For detailed help, execute `poetry run python schoology_extractor/main.py -h`.

```bash
poetry install
poetry run python.exe schoology_extractor/main.py -k your-schoology-client-key -s your-schoology-client-secret  -g csv-of-grading-periods
```

## Test Coverage Report

```bash
poetry run coverage run -m pytest

poetry run coverage report
```

## Output

Four files in the project(or the specified output) directory:

-   `users.csv`
-   `sections.csv`
-   `assignments.csv`
-   `submissions.csv`
