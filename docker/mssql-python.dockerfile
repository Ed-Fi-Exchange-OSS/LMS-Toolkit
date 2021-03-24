# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.

FROM mcr.microsoft.com/mssql/server:2019-latest

# Use root for running apt-get install
USER root

# Install Python 3.8 and make it the default "python" command. Install the
# Poetry package manager. Install ODBC and PostgreSQL development libraries in
# order to support later use of SQL Alchemy.
RUN apt-get update -y && \
    apt-get install software-properties-common -y && \
    add-apt-repository ppa:deadsnakes/ppa -y && \
    apt-get install python3.8-distutils \
        python3.8 \
        python3-pip \
        python3-venv \
        python3-dev \
        libpython3.8-dev \
        unixodbc-dev \
        libpq-dev -y && \
    apt-get clean && \
    rm /usr/bin/python && \
    ln -s /usr/bin/python3.8 /usr/bin/python && \
    python -m pip install --upgrade pip setuptools wheel && \
    mkdir /home/mssql && \
    chown mssql /home/mssql

# Standard SQL Server port
EXPOSE 1433

# Switch back to mssql user for remainder of the setup
USER mssql

# Create an empty profile, and then install Poetry
RUN touch ~/.profile && \
    wget -qO- https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -

# Run SQL Server
ENTRYPOINT /opt/mssql/bin/sqlservr
