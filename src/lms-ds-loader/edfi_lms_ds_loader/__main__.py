# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.

"""
A utility for loading CSV files in the Learning Management System Unified Data
Model (LMS-UDM) into a Learning Management System Data Store (LMS-DS) database.

call `python . -h` for a detailed listing of command arguments.
"""

import logging
import os
import sys

from sqlalchemy import create_engine

from edfi_lms_ds_loader.argparser import parse_arguments
from edfi_lms_ds_loader.lms_filesystem_provider import LmsFilesystemProvider
from edfi_lms_ds_loader.file_processor import FileProcessor
from edfi_lms_ds_loader.migrator import migrate


def _configure_logging(verbose: bool):
    default_level = "INFO"
    if verbose:
        default_level = "DEBUG"
        logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)

    logging.basicConfig(
        handlers=[
            logging.StreamHandler(sys.stdout),
        ],
        format="%(asctime)s - %(levelname)s - %(message)s",
        level=os.environ.get("LOGLEVEL", default_level),
    )


def main():

    arguments = parse_arguments(sys.argv[1:])
    _configure_logging(arguments.verbose)

    db_engine = create_engine(arguments.connection_string)

    migrate(db_engine)

    # TODO: refactoring...
    # - make db_engine a parameter for the file processor
    # - functional, not class
    # - move logging completely into the other classes
    # - ensure this script can easily be called from another program

    logging.info("Starting filesystem processing...")
    fs = LmsFilesystemProvider(arguments.csv_path)
    fs.get_all_files()

    processor = FileProcessor(fs, arguments.get_db_operations_adapter())
    processor.load_lms_files_into_database()


if __name__ == "__main__":
    main()
