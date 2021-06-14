# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.

from sqlalchemy.engine.result import ResultProxy as sa_Result
from sqlalchemy.engine import Engine as sa_Engine
from sqlalchemy.exc import ProgrammingError
from sqlalchemy.orm import Session as sa_Session


def _exec(connection_string: str, statement: str) -> int:
    """This is a wrapper function that will not be unit tested."""

    assert statement.strip() != "", "Argument `statement` cannot be whitespace"

    def __callback(session: sa_Session) -> sa_Result:
        result: sa_Result = session.execute(statement)
        return result

    result = execute_transaction(self.engine, __callback)

    if result:
        return int(result.rowcount)

    return 0


