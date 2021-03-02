# lms-ds-loader

The Ed-Fi LMS Data Store Loader is a utility for loading CSV files in the
Learning Management System Unified Data Model (LMS-UDM) into a Learning
Management System Data Store (LMS-DS) database.

Limitations as of March 2021:

* Data loads only supports SQL Server (tested on MSSQL 2019).
* Only supports loading User files.
* Does not perform updates or deletes, and will throw an error if trying to
  reload an existing record.

## Getting Started

1. SQL Server support requires the Microsoft ODBC 17 driver, which is newer than
   the ones that come with most operating systems.
   * Windows: `choco install sqlserver-odbcdriver`
   * [Linux
     instructions](https://docs.microsoft.com/en-us/sql/connect/odbc/linux-mac/installing-the-microsoft-odbc-driver-for-sql-server?view=sql-server-ver15)
     (has not been tested yet)
1. Requires Python 3.8+ and Poetry.
1. Install required Python packages:

   ```bash
   poetry install
   ```

1. The database account used when running the tool needs to be a member of the
   following roles in the destination database:

   * db_datareader
   * db_datawriter
   * db_ddladmin

Note that the tool automatically manages deployment of the LMS-DS tables into
the destination database, under the `lms` schema.

## Running the Tool

For detailed help, execute `poetry run python edfi_lms_ds_loader -h`.

Sample call using full integrated security, loading from the sample files
directory:

```bash
poetry run python edfi_lms_ds_loader --server localhost --dbname lms_toolkit --useintegratedsecurity --csvpath ../../docs/sample-out
```

## Dev Operations

1. Style check: `poetry run flake8`
1. Static typing check: `poetry run mypy .`
1. Run unit tests: `poetry run pytest`
1. Run unit tests with code coverage: `poetry run coverage run -m pytest`
1. View code coverage: `poetry run coverage report`

_Also see
[build.py](https://github.com/Ed-Fi-Exchange-OSS/LMS-Toolkit/blob/main/docs/build.md)_ for
use of the build script.

## Adding New Migrations

1. Create SQL Server and PostgreSQL SQL scripts under
   `edfi_lms_ds_loader/scripts/<engine name>`, using the same file name for
   both.
1. Use `;` (semi-colon) terminators at the end of each SQL statement for both
   languages. Do not use `GO` in the SQL Server files, as the application is not
   coded to parse it.
1. Add the new script name to the `MIGRATION_SCRIPTS` constant at the top of
   `edfi_lms_ds_loader/migrator.py`.

## Legal Information

Copyright (c) 2021 Ed-Fi Alliance, LLC and contributors.

Licensed under the [Apache License, Version 2.0](https://github.com/Ed-Fi-Exchange-OSS/LMS-Toolkit/blob/main/LICENSE) (the "License").

Unless required by applicable law or agreed to in writing, software distributed
under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR
CONDITIONS OF ANY KIND, either express or implied. See the License for the
specific language governing permissions and limitations under the License.

See [NOTICES](https://github.com/Ed-Fi-Exchange-OSS/LMS-Toolkit/blob/main/NOTICES.md) for
additional copyright and license notifications.
