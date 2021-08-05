# lms-ds-loader

The Ed-Fi LMS Data Store Loader is a utility for loading CSV files in the
Learning Management System Unified Data Model (LMS-UDM) into a Learning
Management System Data Store (LMS-DS) database.

The application processes each file in the input file system by date order, as
indicated in the file name. If a record is in a file one day, and missing on the
next day, then the system "soft deletes" that record by setting the current
timestamp into the `deletedat` column. Similarly, if a previously soft deleted record
reappears later, the record is "un-soft deleted" and updated with any new values.

This functionality requires that a root level directory only contains files for
one LMS provider. Thus if an education organization uses multiple LMS providers,
then each LMS Extractor needs to write files to a separate, dedicated directory,
and the LMS DS Loader must be run once for each extractor's output directory.

## What's New

* Version 1.1:
  * The SQL script names have been modified so that it is easier to add
    new scripts in the future. If you have previously run version 1.0.0,
    then you will need to run the following script once manually before
    running the 1.1.x version of this tool:

    <details>
    <summary>SQL Update Script</summary>
    <div>
    <code>
    update lms.MigrationJournal set script = '0001_initialize_lms_database' where script = 'initialize_lms_database';
    update lms.MigrationJournal set script = '0002_create_processed_files_table' where script = 'create_processed_files_table';
    update lms.MigrationJournal set script = '0003_create_user_tables' where script = 'create_user_tables';
    update lms.MigrationJournal set script = '0004_create_section_tables' where script = 'create_section_tables';
    update lms.MigrationJournal set script = '0005_create_assignment_tables' where script = 'create_assignment_tables';
    update lms.MigrationJournal set script = '0006_create_section_association_tables' where script = 'create_section_association_tables';
    update lms.MigrationJournal set script = '0007_create_assignment_submission_tables' where script = 'create_assignment_submission_tables';
    update lms.MigrationJournal set script = '0008_create_section_activity_tables' where script = 'create_section_activity_tables';
    update lms.MigrationJournal set script = '0009_create_system_activity_tables' where script = 'create_system_activity_tables';
    update lms.MigrationJournal set script = '0010_create_attendance_tables' where script = 'create_attendance_tables';
    update lms.MigrationJournal set script = '0011_remove_startdate_enddate_from_sectionassociation' where script = 'remove_startdate_enddate_from_sectionassociation';
    update lms.MigrationJournal set script = '0012_add_mapping_columns_for_edfi_student_and_section' where script = 'add_mapping_columns_for_edfi_student_and_section';
    </code>
    </div>
    </details>

## Limitations as of April 2021

* This tool only supports SQL Server (tested on MSSQL 2019). PostgreSQL support
  will be added at a future data.

## Getting Started

1. SQL Server support requires the Microsoft ODBC 17 driver, which is newer than
   the ones that come with most operating systems.
   * Windows: `choco install sqlserver-odbcdriver`
   * [Linux
     instructions](https://docs.microsoft.com/en-us/sql/connect/odbc/linux-mac/installing-the-microsoft-odbc-driver-for-sql-server?view=sql-server-ver15)
     (has not been tested yet)
1. Requires Python 3.9+ and Poetry.
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

## Configuration

Supported parameters:

| Description                               | Required            | Command Line Argument             | Environment Variable     |
| ----------------------------------------- | ------------------- | --------------------------------- | ------------------------ |
| CSV file path                             | yes                 | `-c` or `--csvpath`               | CSV_PATH                 |
| Database Engine ("mssql" or "postgresql") | no (default: mssql) | `-e` or `--engine`                | DB_ENGINE                |
| DB Server                                 | yes                 | `-s` or `--server`                | DB_SERVER                |
| DB Port                                   | no (default: 1433)  | `--port`                          | DB_PORT                  |
| DB Name                                   | yes                 | `-d` or `--dbname`                | DB_NAME                  |
| DB Username **                            | no (no default)     | `-u` or `--username`              | DB_USERNAME              |
| DB Password **                            | no (no default)     | `-p` or `--password`              | DB_PASSWORD              |
| Use integrated security **                | no (default: false) | `-i` or `--useintegratedsecurity` | USE_INTEGRATED_SECURITY  |
| Log level*                                | no (default: INFO)  | `-l` or `--log-level`             | LOG_LEVEL                |
| Encrypt db connection                     | no (default: False) | `-n` or `--encrypt`               | ENCRYPT_SQL_CONNECTION   |
| Trust db server certificate               | no (default: False) | `-t` or `--trust-certificate`     | TRUST_SERVER_CERTIFICATE |

\* Valid values for the optional _log level_:

* DEBUG
* INFO(default)
* WARNING
* ERROR
* CRITICAL

\** If using integrated security, DB Username and password won't be required,
otherwise they are required.

## Running the Tool

For detailed help, execute `poetry run python edfi_lms_ds_loader -h`.

Sample call using full integrated security, loading from the sample files
directory:

```bash
poetry run python edfi_lms_ds_loader \
  --server localhost \
  --dbname lms_toolkit \
  --useintegratedsecurity \
  --csvpath ../../docs/sample-out
```

## Developer Notes

### Database-Enabled Integration Tests

This package contains SQL Server-integrated tests, in addition to the standard
unit tests. The specialized tests are in the `tests_integration_sql` directory
and they will run automatically if you call `pytest` with no arguments.

Before running the tests, create an empty SQL Server database named
"test_integration_lms_toolkit": `sqlcmd -Q "create database
test_integration_lms_toolkit"`. This is required to run the SQL Server
integration pytests.

To run only the _unit tests_: `poetry run pytest tests`. To run only the
integration tests, `poetry run pytest tests_integration_sql`.

#### Writing New Tests

Please note and follow the existing pattern for database-enabled integration
tests, as this pattern was carefully tuned to support use of database
transactions for rolling back changes and thereby leaving behind a clean
database.

### Dev Operations

1. Style check: `poetry run flake8`
1. Static typing check: `poetry run mypy .`
1. Run unit tests: `poetry run pytest`
1. Run unit tests with code coverage: `poetry run coverage run -m pytest`
1. View code coverage: `poetry run coverage report`

_Also see
[build.py](https://github.com/Ed-Fi-Exchange-OSS/LMS-Toolkit/blob/main/docs/build.md)_ for
use of the build script.

### Adding New Migrations

1. Create SQL Server and PostgreSQL SQL scripts under
   `edfi_lms_ds_loader/scripts/<engine name>`, using the same file name for
   both. Start from the artifact created by MetaEd, and then update the script
   with these modifications:
   * Remove the `Id` column and the default constraint for that column.
   * Add a `DeletedAt` column as a nullable `Datetime2`.
   * Duplicate the table definition and prefix the duplicate with "stg_".
   * In the staging table, change the `xyzIdentifier` primary key column name to
     `StagingId`, and leave out the `DeletedAt` column.
1. Use `;` (semi-colon) terminators at the end of each SQL statement for both
   languages. Do not use `GO` in the SQL Server files, as the application is not
   coded to parse it.
1. Add the new script name to the `MIGRATION_SCRIPTS` constant at the top of
   `edfi_lms_ds_loader/migrator.py`.

### Adding New Files Uploads

1. Create the required table and staging table in a new migration.
1. Ensure that the `file-utils` shared library correctly maps the data types for
   the new file.
1. Update the `edfi_lms_ds_loader/loader_facade.py` to pull in the additional
   file type and upload it.

## Legal Information

Copyright (c) 2021 Ed-Fi Alliance, LLC and contributors.

Licensed under the [Apache License, Version 2.0](https://github.com/Ed-Fi-Exchange-OSS/LMS-Toolkit/blob/main/LICENSE) (the "License").

Unless required by applicable law or agreed to in writing, software distributed
under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR
CONDITIONS OF ANY KIND, either express or implied. See the License for the
specific language governing permissions and limitations under the License.

See [NOTICES](https://github.com/Ed-Fi-Exchange-OSS/LMS-Toolkit/blob/main/NOTICES.md) for
additional copyright and license notifications.
