# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.

"""
Knows how to navigate the standard filesystem used by the Ed-Fi LMS Exporter
packages.
"""

import os

from typing import List


class LmsFilesystemProvider:

    base_path = ""
    Users: List[str] = []

    def __init__(self, base_path):
        self.base_path = base_path

    def get_all_files(self):
        if not os.path.exists(self.base_path):
            raise OSError(f"Path {self.base_path} does not exist.")

        def _get_user_files():
            user_path = os.path.join(self.base_path, "Users")

            if os.path.exists(user_path):
                self.Users = os.scandir(user_path)

        _get_user_files()

        return self
