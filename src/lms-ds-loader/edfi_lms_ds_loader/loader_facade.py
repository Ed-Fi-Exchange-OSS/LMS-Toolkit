# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.

import logging
from typing import Type

from sqlalchemy import create_engine

from edfi_lms_ds_loader.file_processor import FileProcessor
from edfi_lms_ds_loader.helpers.argparser import MainArguments
from edfi_lms_ds_loader.lms_filesystem_provider import LmsFilesystemProvider
from edfi_lms_ds_loader.migrator import migrate

logger = logging.getLogger(__name__)


def _migrate(arguments: Type[MainArguments]):
    db_engine = create_engine(arguments.connection_string)

    logger.info("Begin database auto-migration...")
    migrate(db_engine)
    logger.info("Done with database auto-migration.")


def _processFiles(arguments: Type[MainArguments]):

    # TODO: refactoring...
    # - make db_engine a parameter for the file processor
    # - functional, not class

    logging.info("Starting filesystem processing...")
    fs = LmsFilesystemProvider(arguments.csv_path)
    fs.get_all_files()

    processor = FileProcessor(fs, arguments.get_db_operations_adapter())
    processor.load_lms_files_into_database()
    logging.info("Done with filesystem processing.")


def run(arguments: Type[MainArguments]):
    _migrate(arguments)
    _processFiles(arguments)
