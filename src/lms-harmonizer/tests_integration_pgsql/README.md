# Integration test setup

These are fully end-to-end tests, where the Harmonizer application is
running from the command line, as opposed to the tests directly exercising
one module or another.

The integration tests require a PostgreSQL database to run. If you do not have a
local PostgreSQL instance, you can start one up in
[docker](../../../eng/docker). Database initialization requires that you have
the `psql` command available in your command path or in a configuration setting
(`psql`).

## Command Line Examples

1. Run integration tests when providing all configuration via `.env` file (you
   can copy the `.env.example` file to `.env` and edit for your own settings):

   ```bash
   poetry run pytest tests_integration_pgsql
   ```

1. Run integration tests with defaults:

   ```bash
   poetry run pytest tests_integration_pgsql --password=p1234
   ```

1. Run integration tests with override for port and username

   ```bash
   poetry run pytest tests_integration_pgsql --password=p1234 --username=joe --port 5402
   ```

## Configuration

Supported parameters:

| Description                | Command Line Argument  | Environment Variable | Default                         |
| -------------------------- | ---------------------- | -------------------- | ------------------------------- |
| DB Server                  | `--server`             | DB_SERVER            | localhost                       |
| DB Port                    | `--port`               | DB_PORT              | 5432                            |
| DB Name                    | `--dbname`             | DB_NAME              | test_harmonizer_lms_toolkit     |
| DB Username                | `--username`           | DB_USER              | postgres                        |
| DB Password                | `--password`           | PGPASSWORD           | _none_                          |
| Skip the database teardown | `--skip-teardown True` | SKIP_TEARDOWN        | False                           |
| Full path to `psql`        | `--psql_cli`           | PSQL_CLI             | psql (assuming in shell's path) |
