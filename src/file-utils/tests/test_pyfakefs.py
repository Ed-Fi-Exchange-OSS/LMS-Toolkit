# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.

import pytest


def describe_will_this_fail():
    @pytest.fixture
    def fixture(fs):
        fs.os = "linux"

    def it_should_not_fail(fs, fixture):
        assert 1 == 1
