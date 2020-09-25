# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.

from lib.zoomRequest import get


def listUsers():
    users = get("/users")
    # here we should handle the pagination and return a list of all users
    return users["users"]
