# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.

"""
placeholder
"""

import sys

from argparser import parse_arguments
from lms_filesystem_provider import LmsFilesystemProvider
from file_processor import FileProcessor


def main():
    arguments = parse_arguments(sys.argv[1:])

    fs = LmsFilesystemProvider(arguments.csv_path)
    fs.get_all_files()

    processor = FileProcessor(fs, arguments.connection_string)
    processor.load_lms_files_into_database()


if __name__ == "__main__":
    main()
