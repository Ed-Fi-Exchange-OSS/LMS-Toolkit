#!/bin/bash
source ~/.profile
# echo $PATH

#wait for sqlservr to start up
sleep 10s

# Run the loader
cd /app/lms-ds-loader
poetry run python edfi_lms_ds_loader \
    -s localhost \
    -d LMS \
    -u sa \
    -p "$SA_PASSWORD" \
    -c /app/data \
    > /app/out/output.txt

# TODO: decide how we want to capture the output.
