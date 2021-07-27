# This tool is a back-door for loading Descriptor XML files directly into the
# ODS database. This is not a recommended practice and should only be used
# for local database development.

import sys

from configargparse import ArgParser  # type: ignore
from sqlalchemy import create_engine

from tests.data_helpers import load_lms_descriptors


def get_conn_string_from_args() -> str:

    parser = ArgParser()
    parser.add(
        "--server",
        action="store",
        default="localhost",
        help="Database server name or IP address",
    )
    parser.add(
        "--port", action="store", default="1433", help="Database server port number"
    )
    parser.add(
        "--dbname",
        action="store",
        default="test_analytics_middle_tier_engage",
        help="Name of the test database",
    )
    parser.add(
        "--useintegratedsecurity",
        action="store",
        default=True,
        help="Use Integrated Security for the database connection",
    )
    parser.add(
        "--username",
        action="store",
        help="Database username when not using integrated security",
    )
    parser.add(
        "--password",
        action="store",
        help="Database user password, when not using integrated security",
    )

    parsed = parser.parse_args(sys.argv[1:])

    server = parsed.server
    port = parsed.port or "1433"
    db_name = parsed.dbname
    username = parsed.username
    password = parsed.password

    integrated = parsed.useintegratedsecurity

    if integrated:
        return f"mssql+pyodbc://{server},{port}/{db_name}?driver=ODBC+Driver+17+for+SQL+Server&Trusted_Connection=yes"
    else:
        return f"mssql+pyodbc://{username}:{password}@{server},{port}/{db_name}?driver=ODBC+Driver+17+for+SQL+Server"


if __name__ == "__main__":
    conn_string = get_conn_string_from_args()
    engine = create_engine(conn_string)

    load_lms_descriptors(engine)
