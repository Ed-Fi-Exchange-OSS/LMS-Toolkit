# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.

import pytest

INPUT_DIRECTORY = './input'


def _setup_empty_filesystem(fs):
    fs.path_separator = "/"
    fs.is_windows_fs = False
    fs.is_macos = False
    fs.create_dir(INPUT_DIRECTORY)


def describe_will_this_fail():
    def describe_one_more_level_nesting():
        @pytest.fixture
        def fixture(fs):
            _setup_empty_filesystem(fs)

        def it_should_not_fail(fs, fixture):
            assert 1 == 1
