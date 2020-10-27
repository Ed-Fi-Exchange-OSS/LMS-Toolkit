# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.

from sqlalchemy import types

ROLE_COLUMN_TYPES_MAPPING = dict({'links': types.JSON})

SECTION_COLUMN_TYPES_MAPPING = {
    'grading_periods': types.JSON,
    'meeting_days': types.JSON,
    'options': types.JSON,
    'links': types.JSON,
}
