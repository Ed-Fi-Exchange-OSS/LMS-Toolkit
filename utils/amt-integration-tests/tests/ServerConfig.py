# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.

from dataclasses import dataclass


@dataclass(frozen=True)
class ServerConfig:
    useintegratedsecurity: str
    server: str
    port: str
    db_name: str
    username: str
    password: str
    skip_teardown: bool

    def get_pyodbc_connection_string(self) -> str:
        port = self.port or "1433"

        if self.useintegratedsecurity:
            return f"mssql+pyodbc://{self.server},{port}/{self.db_name}?driver=ODBC+Driver+17+for+SQL+Server?Trusted_Connection=yes"
        else:
            return f"mssql+pyodbc://{self.username}:{self.password}@{self.server},{port}/{self.db_name}?driver=ODBC+Driver+17+for+SQL+Server"

    def get_dotnet_connection_string(self) -> str:

        port = self.port or "1433"
        con_string = f"server={self.server},{port};database={self.db_name}"

        if self.useintegratedsecurity:
            return f"{con_string};integrated security=SSPI"
        else:
            return f"{con_string};user id={self.username};password={self.password}"
