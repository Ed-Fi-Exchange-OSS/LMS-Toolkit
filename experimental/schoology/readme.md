# Schoology Assignment Data

Requirements:

* Python 3.8.x
* Poetry

Execution:

```bash
poetry install
poetry run python main.py
```

Output: four files in the `./output` directory:

* `users-<datetimestamp>.csv`
* `sections-<datetimestamp>.csv`
* `assignments-<datetimestamp>.csv`
* `submissions-<datetimestamp>.csv`

**Note**: some of these CSV files contain structured data in the rows. This is not
ideal and will be refactored. For example, the assignments file contains a
single row for each assignment. If all students received the assignment, then
the final column will have the value "[]" for an empty list. If only a subset of
students are assigned, then that final column will contain a list of the
assigned students' names. In the long term this will be transformed so that each
assignment-student combination will have a separate row in the output file.
