# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.

import requests
import os

def get(url):
    base_url = os.getenv("CANVAS_BASE_URL")
    auth_token = os.getenv("CANVAS_ACCESS_TOKEN")
    r = requests.get(
        base_url + "/" + url,
        headers={ "Authorization" : f"Bearer {auth_token}" },)
    return r.json()
