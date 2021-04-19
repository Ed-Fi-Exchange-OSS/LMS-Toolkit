# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.

# This script is for running the process on a Windows workstation

docker rm -f test-lms-ds-loader
docker run --name test-lms-ds-loader -e 'ACCEPT_EULA=Y' -e 'SA_PASSWORD=yourStrong(!)Password' test-lms-ds-loader:latest
docker logs test-lms-ds-loader
