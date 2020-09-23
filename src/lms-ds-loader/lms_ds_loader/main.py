# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.

"""
The following comments will be cleaned up before finishing this module. This is just an outline of the task:

# 1 Read arguments
# 2 Validate arguments
# 3 Initially only look in the Users folder, looking for files like /ed-fi-udm-lms/users/<YYYY-mm-dd-HH-MM-SS>.csv
# 4 For each file
# 4.1 See if it is already loaded
# 4.2 If not, open file using Pandas
# 4.3 Query for existing user rows
# 4.4 Insert rows that aren't already present
"""

import sys

from argparser import parse_arguments

# TODO: keeping this around until I need it, at which time it will move elsewhere
# def test_sql_connection():
# import pandas as pd
# import pyodbc
# import sqlalchemy as sal
# from sqlalchemy import create_engine
# engine = sal.create_engine("mssql+pyodbc://localhost/fizz?driver=SQL Server?Trusted_Connection=yes")
# conn = engine.connect()
# tables = pd.read_sql_query("SELECT * FROM INFORMATION_SCHEMA.TABLES", engine)
# print(tables)
# conn.close()


def main():
    arguments = parse_arguments(sys.argv[1:])
    print(arguments)


if __name__ == "__main__":
    main()
