# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.

from edfi_lms_extractor_lib.helpers.decorators import catch_exceptions


def describe_given_function_that_does_not_throw_error() -> None:
    def it_returns_true() -> None:
        result = catch_exceptions(lambda: 1/1)()
        assert result is True


def describe_given_function_throws_an_error() -> None:
    def it_returns_false() -> None:
        result = catch_exceptions(lambda: 1/0)()
        assert result is False
