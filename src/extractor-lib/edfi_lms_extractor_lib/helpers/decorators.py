# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.

import logging
from typing import Callable


def catch_exceptions(func: Callable) -> Callable[..., bool]:
    logger = logging.getLogger(__name__)

    def callable_function(*args, **kwargs) -> bool:
        try:
            func(*args, **kwargs)
            return True
        except BaseException as e:
            logger.exception("An exception occurred: %s", e)
            return False

    return callable_function
