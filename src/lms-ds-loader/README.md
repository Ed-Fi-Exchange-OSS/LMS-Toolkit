# lms-ds-loader

A utility for loading CSV files in the Learning Management System Unified Data
Model (LMS-UDM) into a Learning Management System Data Store (LMS-DS) database.

Limitations as of September 23, 2020:

* Only supports SQL Server (tested on MSSQL 2019)
* Only supports loading User files
* Does not perform updates or deletes, and will throw an error if trying to
  reload an existing record.

## Getting Started

1. Requires Python 3.8+ and Poetry.
1. Install required Python packages:

   ```bash
   poetry install
   ```

1. Run the two SQL scripts in `src/lms-ds-installer/mssql` in a database.

## Running the Tool

For detailed help, execute `poetry run lms_ds_loader/main.py -h`.

Sample call using full integrated security, loading from the sample files
directory:

```bash
poetry run python ./lms_ds_loader/main.py --server localhost --dbname fizz --useintegratedsecurity --csvpath ../../docs/sample-out
```

## Dev Operations

1. Run unit tests: `poetry run pytest`
1. Run unit tests with XLM report: `poetry run pytest --junitxml="pytest.xml"`
1. Run unit tests with code coverage: `poetry run coverage run -m pytest`
1. View coverage report in the console: `poetry run coverage report`
1. Generate an XML coverage report: `poetry run coverage xml` generates file
   `coverage.xml`
