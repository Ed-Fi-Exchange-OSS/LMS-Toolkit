# Integration test setup

These are fully end-to-end tests, where the Harmonizer application is
running from the command line, as opposed to the tests directly exercising
one module or another.

The integration tests require a SQL Server database to run. If you do not have a
local SQL Server instance, you can start one up in
[docker](../../../eng/docker).

By default, the tests use integrated security with a database name of
"test_harmonizer_lms_toolkit" on the standard port of 1433.  This can be
overridden via command line switches in a similar fashion as the command line
switches from the harmonizer itself.

Note that all values have defaults, and one difference from the harmonizer is
that integrated security is true by default. DB Username and DB Password
are ignored when integrated security is set to true.

## Examples

1. Run integration tests with defaults:

   ```bash
   poetry run pytest tests_integration_sql
   ```

1. Run integration tests with username/password security:

   ```bash
   poetry run pytest tests_integration_sql --useintegratedsecurity=false --username=joe --password=p1234
   ```

## Configuration

Supported parameters:

| Description                | Command Line Argument     | Environment Variable    | Default                     |
| -------------------------- | ------------------------- | ----------------------- | --------------------------- |
| DB Server                  | `--server`                | DB_SERVER               | localhost                   |
| DB Port                    | `--port`                  | DB_PORT                 | 1433                        |
| DB Name                    | `--db_name`               | DB_NAME                 | test_harmonizer_lms_toolkit |
| Use integrated security    | `--useintegratedsecurity` | USE_INTEGRATED_SECURITY | true                        |
| DB Username                | `--username`              | DB_USER                 | localuser                   |
| DB Password                | `--password`              | DB_PASSWORD             | localpassword               |
| Skip the database teardown | `--skip-teardown True`    | SKIP_TEARDOWN           | False                       |
