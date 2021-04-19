# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.

# Copies files into a temporary diretory so that the Dockerfile can reference
# them without ascending beyond the parent directory.

mkdir -p tmp

cp -rf ./src/lms-ds-loader/edfi_lms_ds_loader docker/test-lms-ds-loader/tmp/
cp -rf ./src/lms-ds-loader/pyproject.toml docker/test-lms-ds-loader/tmp/
cp -rf ./src/lms-ds-loader/poetry.lock docker/test-lms-ds-loader/tmp/
cp -rf ./src/lms-ds-loader/README.md docker/test-lms-ds-loader/tmp/
cp -rf ./docs/sample-out docker/test-lms-ds-loader/tmp/
