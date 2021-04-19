# Docker Support for the Ed-Fi LMS Toolkit

These Docker-related files are used primarily for evaluation and testing,
although they might also be useful as building blocks for a production system.
Each file is described below.

## mssql-python.dockerfile

Creates an image with SQL Server 2019 (latest patch) and Python 3.8. Typically
one would not install client tools such as Python on the database server. This
container is intended for use in database integration testing, where it is
temporarily convenient to run Python scripts directly on the database host.

Build:

```bash
docker build -f mssql-python.dockerfile -t mssql-python:latest .

# Optional version tags
docker build -f mssql-python.dockerfile -t mssql-python:sql2019-py38-latest .
```

The PowerShell `build.ps1` script runs the first command above.

Run, with the TCP/IP port mapped for localhost access:

```bash
docker run -e 'ACCEPT_EULA=Y' -e 'SA_PASSWORD=yourStrong(!)Password' -p 1433:1433 --name mssql -d mssql-python:latest

# If you already have a local SQL Server instance running, change the left side
# of the port mapping
docker run -e 'ACCEPT_EULA=Y' -e 'SA_PASSWORD=yourStrong(!)Password' -p 1434:1433 --name mssql -d mssql-python:latest
```

When specifying an alternate port, connect to the image with server name `localhost,1434`.

## test-lms-ds-loader directory

This dockerfile builds on the mssql-python container to run the LMS-DS Loader
using the sample output files from the repository. On a Windows localhost, use
`build.ps1` to build the image and `run.ps1` to run it. The Entrypoint in theory
should set "success=true" as an output in GitHub Actions.

## Current Status 2021-04-19

The container action runs. Right now `poetry` is not being installed correctly.
Getting the following errors in the [latest
run])(https://github.com/Ed-Fi-Alliance-OSS/LMS-Toolkit/runs/2382302900):

```none
/app/entrypoint.sh: line 16: poetry: command not found
/app/entrypoint.sh: line 24: 127: command not found
```

While we do not have a complete integration test at this point, the pieces are
coming together and the original timebox has been exhausted. Outcomes:

* Built an MSSQL / Python 3.9 container
* Learned how to prep and start a container in GitHub Actions

Next steps

* When built locally, poetry worked. It should be in the container that was pushed to Docker Hub.
* Work output formatting / error detection.
* Build out the sample files to test more scenarios.
