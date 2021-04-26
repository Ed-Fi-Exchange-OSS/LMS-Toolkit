# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.

"""Build automation scripts"""

import os
import subprocess
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

For example, to run unit tests with code coverage, optimized for TeamCity
output, on utility `lms-ds-loader`:

> ./build.py coverage:xml lms-ds-loader
"""
    print(message)
    exit(-1)


def _run_command(command: List[str], exit_immediately: bool = True):

    print('\033[95m' + " ".join(command) + '\033[0m')

    # Some system configurations on Windows-based CI servers have trouble
    # finding poetry, others do not. Explicitly calling "cmd /c" seems to help,
    # though unsure why.

    if (os.name == "nt"):
        # All versions of Windows are "nt"
        command = ["cmd", "/c", *command]

    script_dir = os.path.dirname(os.path.realpath(sys.argv[0]))

    package_name = sys.argv[2]

    package_dir = os.path.join(script_dir, "..", "src", package_name)
    if not os.path.exists(package_dir):
        package_dir = os.path.join(script_dir, "..", "utils", package_name)

        if not os.path.exists(package_dir):
            raise RuntimeError(f"Cannot find package {package_name}")

    result = subprocess.run(command, cwd=package_dir)

    if exit_immediately:
        exit(result.returncode)

    if result.returncode != 0:
        exit(result.returncode)


def _run_install():
    _run_command([
        "poetry",
        "install"
    ])


def _run_tests():
    _run_command([
        "poetry",
        "run",
        "pytest",
        "tests",
    ])


def _run_coverage():
    _run_command([
        "poetry",
        "run",
        "coverage",
        "run",
        "-m",
        "pytest",
        "tests",
    ], exit_immediately=False)
    _run_command([
        "poetry",
        "run",
        "coverage",
        "report",
    ], exit_immediately=False)


def _run_coverage_html():
    _run_command([
        "poetry",
        "run",
        "coverage",
        "run",
        "-m",
        "pytest",
        "tests",
    ], exit_immediately=False)
    _run_command([
        "poetry",
        "run",
        "coverage",
        "html",
    ], exit_immediately=False)


def _run_coverage_xml():
    _run_command([
        "poetry",
        "run",
        "coverage",
        "run",
        "-m",
        "pytest",
        "tests",
    ], exit_immediately=False)
    _run_command([
        "poetry",
        "run",
        "coverage",
        "xml"
    ])


def _run_lint():
    _run_command([
        "poetry",
        "run",
        "flake8"
    ])


def _run_typecheck():
    _run_command([
        "poetry",
        "run",
        "mypy"
    ])


def _run_typecheck_xml():
    _run_command([
        "poetry",
        "run",
        "mypy",
        "--junit-xml",
        "mypy.xml"
    ])


def _run_build():
    _run_command([
        "poetry",
        "build"
    ])


def _run_publish():
    shutil.rmtree('dist', ignore_errors=True)

    _run_command([
        "poetry",
        "build"
    ], exit_immediately=False)

    _run_command([
        "poetry",
        "run",
        "twine",
        "upload",
        "dist/*"
    ])


if __name__ == "__main__":
    if not sys.version_info >= (3, 8):
        print("This program requires Python 3.8 or newer.", file=sys.stderr)
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
    }

    switcher.get(sys.argv[1], _display_help)()
