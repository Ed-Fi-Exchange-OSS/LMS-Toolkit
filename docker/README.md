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
using the sample output files from the repository.

| More work is needed to capture test results, this is really just a POC.
Running in the container this way might not even be a good idea |
| -- |

```bash
cd test-lms-ds-loader
docker build -t test-lms-ds-loader:latest .
docker run --name test-lms-ds-loader -e 'ACCEPT_EULA=Y' -e 'SA_PASSWORD=yourStrong(!)Password' -d test-lms-ds-loader:latest
```

The PowerShell `build.ps1` script runs the `docker build` command above. The run
command above lets sql server keep running, which is annoying and will need to
be changed for the real (non spike) work. Control-c to exit from the log output
once you see "The tempdb database has 8 data file(s) and no more messages are
appearing.

For some reason the entrypoint file is not running. Probably a simple mistake in
the dockerfile - perhaps along the lines of the "parent" `mssql-python`
dockerfile having an `ENTRYPOINT` and maybe that is causing the `CMD` in
`test-lms-ds-loader` from running?

The `poetry install` command in the dockerfile is not working correctly either.
Although there is no error, I'm having to run `poetry install` again manually.
The point in putting into the Dockerfile was to get all the dependencies before
building the image. That might be a strange thing to do. Will need to carefully
think through this architecture in more detail.

```bash
# Connect to the container shell in order to run commands directly within the container
docker exec -it test-lms-ds-loader /bin/bash

# Now you are in the container...
source ~/.profile

# This command actually gives me a warning:
# "The virtual environment found in /app/lms-ds-loader/.venv seems to be broken."
#poetry install

# Do not know what is going on. However, I was able to temporarily work with this...
poetry shell
poetry install

# Now run the test script
cd ../
# want to run this script, but with the above problems, more useful to run manually
# for the moment.
#./entrypoint.sh

python edfi_lms_ds_loader \
    -s localhost \
    -d LMS \
    -u sa \
    -p "$SA_PASSWORD" \
    -c /app/data \
    > /app/out/output.txt

# ERROR: "Cannot open database "LMS" requested by the login."
# Oops, we need a command to create the database. Going to save that for the real work -
# need to close out this spike.

# exit from poetry shell
exit

# exit from docker container
exit

# back to local command prompt - copy output (if there's something worth copying)
#docker cp test-lms-ds-loader:/app/out/output.txt .

# Stop and remove that container
docker rm test-lms-ds-loader -f
```
