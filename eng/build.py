# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.

"""Build automation scripts"""

import os
from subprocess import run
import shutil
import sys
from typing import List


def _display_help():
    message = """Please specify a command followed by a module. Valid commands:

* install
* test
* coverage
* coverage:html
* coverage:xml
* lint
* typecheck
* typecheck:xml
* build
* publish
* ci:test
* ci:integration-test:mssql
* ci:integration-test:pgsql
* ci:publish

For example, to run unit tests with code coverage, optimized for TeamCity
output, on utility `lms-ds-loader`:

> ./build.py coverage:xml lms-ds-loader

When running the integration tests, use environment variables to inject
database settings. Relevant environment variables, with default values shown:

* SQL Server
  * MSSQL_INTEGRATED_SECURITY = True; or set to False
  * MSSQL_USER = "sa"; only used if MSSQL_INTEGRATED_SECURITY is False
  * MSSQL_PASSWORD = ""; will fail if you don't set it
  * MSSQL_HOST = "localhost"
  * MSSQL_PORT = 1433
  * DB_NAME = "test_integration_lms_toolkit"
* PostgreSQL
  * PGSQL_HOST = "localhost"
  * PGSQL_USER = "postgres
  * PGSQL_PASSWORD = "postgres"
  * PGSQL_PORT = 5432
  * DB_NAME = "test_integration_lms_toolkit"
  * PSQL_CLI = "psql"; can change to use exact path to psql executable
"""
    print(message)
    exit(-1)


def _run_command(command: List[str], exit_immediately: bool = True):

    print("\033[95m" + " ".join(command) + "\033[0m")

    # On Windows, must run inside of cmd.exe in order to get the user's $PATH.
    if os.name == "nt":
        # All versions of Windows are "nt"
        command = ["cmd", "/c", *command]

    script_dir = os.path.dirname(os.path.realpath(sys.argv[0]))

    package_name = sys.argv[2]

    package_dir = os.path.join(script_dir, "..", "src", package_name)
    if not os.path.exists(package_dir):
        package_dir = os.path.join(script_dir, "..", "utils", package_name)

        if not os.path.exists(package_dir):
            raise RuntimeError(f"Cannot find package {package_name}")

    result = run(command, cwd=package_dir)

    return_code = result.returncode

    if exit_immediately:
        # Exits the script regardless of the prior return code
        exit(return_code)

    if return_code != 0:
        # Only exits the script for non-zero return code
        exit(return_code)


def _run_install(exit_immediately: bool = True):
    _run_command(["poetry", "install"], exit_immediately)


def _run_tests(exit_immediately: bool = True):
    _run_command(
        [
            "poetry",
            "run",
            "pytest",
            "tests",
        ],
        exit_immediately,
    )


def _run_mssql_tests(exit_immediately: bool = True):

    credentials = list()
    if os.getenv('MSSQL_INTEGRATED_SECURITY', True) is True:
        credentials.append("--useintegratedsecurity=true")
    else:
        credentials.append("--useintegratedsecurity=false")
        credentials.append(f"--username={os.getenv('MSSQL_USER', 'sa')}")
        credentials.append(f"--password={os.getenv('MSSQL_PASSWORD', '')}")

    _run_command(
        [
            "poetry",
            "run",
            "pytest",
            "tests_integration_mssql",
            *credentials,
            f"--server={os.getenv('MSSQL_HOST', 'localhost')}",
            f"--port={os.getenv('MSSQL_PORT', 1433)}",
            f"--dbname={os.getenv('DB_NAME', 'test_integration_lms_toolkit')}"
        ],
        exit_immediately,
    )


def _run_pgsql_tests(exit_immediately: bool = True):
    _run_command(
        [
            "poetry",
            "run",
            "pytest",
            "tests_integration_pgsql/",
            f"--server={os.getenv('PGSQL_HOST', 'localhost')}",
            f"--username={os.getenv('PGSQL_USER','postgres')}",
            f"--password={os.getenv('PGSQL_PASSWORD', 'postgres')}",
            f"--port={os.getenv('PGSQL_PORT', 5432)}",
            f"--dbname={os.getenv('DB_NAME', 'test_integration_lms_toolkit')}",
            f"--psql_cli={os.getenv('PSQL_CLI','psql')}"
        ],
        exit_immediately,
    )


def _run_coverage_without_report():
    _run_command(
        [
            "poetry",
            "run",
            "coverage",
            "run",
            "-m",
            "pytest",
            "tests",
        ],
        exit_immediately=False,
    )


def _run_coverage():
    _run_coverage_without_report()

    _run_command(
        [
            "poetry",
            "run",
            "coverage",
            "report",
        ],
        exit_immediately=True,
    )


def _run_coverage_html(exit_immediately: bool = True):
    _run_coverage_without_report()

    _run_command(
        [
            "poetry",
            "run",
            "coverage",
            "html",
        ],
        exit_immediately,
    )


def _run_coverage_xml():
    _run_command(
        [
            "poetry",
            "run",
            "coverage",
            "run",
            "-m",
            "pytest",
            "tests",
        ],
        exit_immediately=False,
    )

    _run_command(["poetry", "run", "coverage", "xml"], exit_immediately=False)


def _run_lint(exit_immediately: bool = True):
    _run_command(["poetry", "run", "flake8"], exit_immediately)


def _run_typecheck():
    _run_command(["poetry", "run", "mypy"], exit_immediately=True)


def _run_typecheck_xml(exit_immediately: bool = True):
    _run_command(["poetry", "run", "mypy", "--junit-xml", "mypy.xml"], exit_immediately)


def _run_build(exit_immediately: bool = True):
    _run_command(["poetry", "build"], exit_immediately)


def _run_publish(exit_immediately: bool = True):
    shutil.rmtree("dist", ignore_errors=True)

    _run_build(False)

    _run_command(["poetry", "run", "twine", "upload", "dist/*"], exit_immediately)


def _run_ci_test():
    """
    Calls the commands required for a continuous unit testing, type-checking, and linting job.
    """
    _run_install(False)
    _run_coverage_html(False)
    _run_typecheck_xml(False)
    _run_lint(True)


def _run_ci_mssql_test():
    """
    Calls the commands required for a continuous integration testing job.
    """
    _run_install(False)
    _run_mssql_tests(False)


def _run_ci_pgsql_test():
    """
    Calls the commands required for a continuous integration testing job.
    """
    _run_install(False)
    _run_pgsql_tests(False)


def _run_ci_publish():
    """
    Calls the commands required for a continuous integration publishing job.
    """
    _run_install(False)
    _run_tests(False)
    _run_publish(True)


if __name__ == "__main__":
    if not sys.version_info >= (3, 9):
        print("This program requires Python 3.9 or newer.", file=sys.stderr)
        exit(-1)

    if len(sys.argv) < 3:
        _display_help()

    switcher = {
        "install": _run_install,
        "test": _run_tests,
        "coverage": _run_coverage,
        "coverage:html": _run_coverage_html,
        "coverage:xml": _run_coverage_xml,
        "lint": _run_lint,
        "typecheck": _run_typecheck,
        "typecheck:xml": _run_typecheck_xml,
        "build": _run_build,
        "publish": _run_publish,
        "ci:test": _run_ci_test,
        "ci:integration-test": _run_ci_mssql_test,
        "ci:integration-test:mssql": _run_ci_mssql_test,
        "ci:integration-test:pgsql": _run_ci_pgsql_test,
        "ci:publish": _run_ci_publish,
    }

    switcher.get(sys.argv[1], _display_help)()
