# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.

from datetime import datetime
import os

USERS = "users"


def _get_file_name() -> str:
    return datetime.now().strftime("%Y-%m-%d-%H-%M-%S") + ".csv"


def get_assignment_file_path(output_directory: str, section_id: int) -> str:
    return os.path.join(output_directory, f"section={section_id}", _get_file_name())


def get_user_file_path(output_directory: str) -> str:
    base_folder = os.path.join(output_directory, USERS)
    if not os.path.exists(base_folder):
        os.mkdir(base_folder)

    return os.path.join(base_folder, _get_file_name())
