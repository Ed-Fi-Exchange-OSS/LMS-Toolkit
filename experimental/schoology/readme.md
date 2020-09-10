# Schoology Assignment Data

This script retrieves and writes out to CSV all students, sections, assignments,
and submissions for the desired grading period(s).

## Requirements

* Python 3.8.x
* Poetry

## Configuration

Configuration is via `.env` file or directly with environment variables listed
below. User's API key and secret are managed at https://app.schoology.com/api.
The grading periods list helps determine which grading periods are of interest -
for example, an organization with school years in one Schoology account would
only want to list the grading periods for the current school year. Run `poetry
run python grading_periods.py` to get a list of grading periods (requires that
the `.env` file has the key and secret values already configured).

* `SCHOOLOGY_KEY=<administrator's API key>`
* `SCHOOLOGY_SECRET=<administrator's API secret>`
* `SCHOOLOGY_GRADING_PERIODS=<csv list of grading period ids>`
* `SCHOOLOGY_OUTPUT_PATH=<output directory>`

For example, the output of the grading_periods script might be:

```none
   grading_period_id                      title
0             825792    Fall Semester 2021-2022
1             825790  Spring Semester 2020-2021
2             822639    Fall Semester 2020-2021
3             825791  Spring Semester 2019-2020
```

If you only want to export data for the 2021 school year, then:

* `SCHOOLOGY_GRADING_PERIODS=825790,822639`

## Execution

```bash
poetry install
poetry run python main.py
```

## Output

Four files in the `./output` directory:

* `users-<datetimestamp>.csv`
* `sections-<datetimestamp>.csv`
* `assignments-<datetimestamp>.csv`
* `submissions-<datetimestamp>.csv`

**Note**: some of these CSV files contain structured data in the rows. This is
not ideal and will be refactored. For example, the assignments file contains a
single row for each assignment. If all students received the assignment, then
the final column will have the value "[]" for an empty list. If only a subset of
students are assigned, then that final column will contain a list of the
assigned students' names. In the long term this will be transformed so that each
assignment-student combination will have a separate row in the output file.
