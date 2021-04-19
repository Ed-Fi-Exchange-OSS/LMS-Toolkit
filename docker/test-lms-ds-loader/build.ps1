# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.

$ErrorActionPreference = "Stop"

# We need to copy the LMS-DS loader and sample files to a local directory so
# that they can be copied into the Docker image.
$tmp = New-Item -Type Directory -Path tmp -Force

Copy-Item -Recurse -Path "../../src/lms-ds-loader/edfi_lms_ds_loader" -Destination $tmp -Force -Exclude ".env"
Copy-Item -Recurse -Path "../../src/lms-ds-loader/pyproject.toml" -Destination $tmp -Force
Copy-Item -Recurse -Path "../../src/lms-ds-loader/poetry.lock" -Destination $tmp -Force
Copy-Item -Recurse -Path "../../src/lms-ds-loader/README.md" -Destination $tmp -Force
Copy-Item -Recurse -Path "../../docs/sample-out" -Destination $tmp -Force

# Now we can build the image
docker build -t test-lms-ds-loader:latest .
