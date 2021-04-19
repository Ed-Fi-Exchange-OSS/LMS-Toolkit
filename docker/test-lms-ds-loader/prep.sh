# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.

# Copies files into a temporary diretory so that the Dockerfile can reference
# them without ascending beyond the parent directory. Note that the directory
# paths are carefully crafted to work when run from within a GitHub action,
# rather than running from a workstation plain Bash prompt

mkdir -p docker/test-lms-ds-loader/tmp/

cp -r ./src/lms-ds-loader/edfi_lms_ds_loader docker/test-lms-ds-loader/tmp/edfi_lms_ds_loader
cp ./src/lms-ds-loader/pyproject.toml docker/test-lms-ds-loader/tmp/
cp ./src/lms-ds-loader/poetry.lock docker/test-lms-ds-loader/tmp/
cp ./src/lms-ds-loader/README.md docker/test-lms-ds-loader/tmp/
cp ./docs/sample-out docker/test-lms-ds-loader/tmp/
