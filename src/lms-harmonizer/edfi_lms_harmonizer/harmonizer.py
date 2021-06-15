# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.

import logging

from sqlalchemy.engine.base import Engine

from edfi_lms_extractor_lib.helpers.decorators import catch_exceptions
from helpers.argparser import MainArguments


logger = logging.getLogger(__name__)


@catch_exceptions
def harmonize_users(engine: Engine) -> None:

    with engine.connect().execution_options(autocommit=True) as connection:
        logger.info("Harmonizing Canvas LMS Users.")
        connection.execute("EXEC lms.harmonize_lmsuser_canvas;")

        logger.info("Harmonizing Google Classroom LMS Users.")
        connection.execute("EXEC lms.harmonize_lmsuser_google_classroom;")

        logger.info("Harmonizing Schoology LMS Users.")
        connection.execute("EXEC lms.harmonize_lmsuser_schoology;")


def run(arguments: MainArguments) -> None:

    engine: Engine = arguments.get_db_engine()
    harmonize_users(engine)
