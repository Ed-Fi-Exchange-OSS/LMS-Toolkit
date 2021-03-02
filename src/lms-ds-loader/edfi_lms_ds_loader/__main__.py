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

from dotenv import load_dotenv
from errorhandler import ErrorHandler  # type: ignore
from sqlalchemy import create_engine

from edfi_lms_ds_loader.helpers.argparser import parse_main_arguments
from edfi_lms_ds_loader.lms_filesystem_provider import LmsFilesystemProvider
from edfi_lms_ds_loader.file_processor import FileProcessor
from edfi_lms_ds_loader.migrator import migrate

# Load configuration
load_dotenv()


logger: logging.Logger
error_tracker: ErrorHandler

arguments = parse_main_arguments(sys.argv[1:])
engine = arguments.engine
connection_string = arguments.connection_string


def _configure_logging():
    global logger
    global error_tracker

    logger = logging.getLogger(__name__)

    level = os.environ.get("LOGLEVEL", "INFO")
    logging.basicConfig(
        handlers=[
            logging.StreamHandler(sys.stdout),
        ],
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
        level=level,
    )
    error_tracker = ErrorHandler()


def main():

    _configure_logging()

    db_engine = create_engine(connection_string)

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
