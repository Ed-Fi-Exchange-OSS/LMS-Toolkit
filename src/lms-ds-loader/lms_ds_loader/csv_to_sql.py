# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.

import pandas as pd
import sqlalchemy as sal


class CsvToSql:
    """
    Reads a CSV file and loads it into a table.

    Parameters
    ----------
    connection_string : str
        Database connection string in PyODBC format.
    """
    def __init__(self, connection_string):
        self.connection_string = connection_string
        self.engine = None

    def _get_engine(self):
        """lazy-load private property"""

        if not self.engine:
            self.engine = sal.create_engine(self.connection_string)

        return self.engine

    def load_file(self, file, table):
        """
        Executes the file read and database upload process.

        Parameters
        ----------
        file : str
            Full path to a file to read.
        table : str
            Name of the destination table, assumed to be in an "lms" schema.
        """
        df = pd.read_csv(file)

        with self._get_engine().connect() as connection:
            df.to_sql(
                table,
                connection,
                schema="lms",
                if_exists="append",
                index=False,
                method="multi",
            )
