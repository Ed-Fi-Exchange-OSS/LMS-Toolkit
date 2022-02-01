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
are ignored when intergrated security is set to true.

## Examples

1. Run integration tests with defaults:

   ```bash
   poetry run pytest tests_integration_mssql
   ```

1. Run integration tests with username/password security:

   ```bash
   poetry run pytest tests_integration_mssql --useintegratedsecurity=false --username=joe --password=p1234
   ```

## Configuration

Supported parameters:

| Description | Command Line Argument | Default |
| ----------- | --------------------- | ------- |
| DB Server | `--server` | localhost |
| DB Port | `--port` | 1433 |
| DB Name | `--dbname` | test_harmonizer_lms_toolkit |
| Use integrated security | `--useintegratedsecurity` | true |
| DB Username | `--username` | localuser |
| DB Password | `--password` | localpassword |
| Skip the database teardown | `--skip-teardown True` | False |
