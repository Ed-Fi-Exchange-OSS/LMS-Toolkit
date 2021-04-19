#!/bin/bash
source ~/.profile

# wait for sqlservr to start up
sleep 30s

# Create the LMS database
/opt/mssql-tools/bin/sqlcmd -S localhost \
    -U sa \
    -P "$SA_PASSWORD" \
    -d master \
    -Q "create database LMS;"

# Run the loader
cd /app
poetry run python edfi_lms_ds_loader \
    -s localhost \
    -d LMS \
    -u sa \
    -p "$SA_PASSWORD" \
    -c /app/sample-out \
    > /app/output.log

if $? == 0; then
    echo "::set-output name=success::true"
else
    echo "::set-output name=success::false"
fi

# Display the log at the command prompt
cat /app/output.log

# Exit SQL Server
kill $(ps aux | grep '[s]qlservr' | awk '{print $2}')
