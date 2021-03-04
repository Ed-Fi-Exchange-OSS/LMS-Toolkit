# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.

import pandas as pd

DISCUSSION_REPLIES_TYPE = "discussion-reply"


def map_to_udm(section_updates_df: pd.DataFrame, section_id: int) -> pd.DataFrame:
    """
    Maps a DataFrame containing Schoology section updates
    into the Ed-Fi LMS Unified Data Model (UDM) format.

    Parameters
    ----------
    section_updates_df: DataFrame
        Pandas DataFrame containing Schoology assignments for a section

    Returns
    -------
    DataFrame
        A LMSSectionActivities-formatted DataFrame

    Notes
    -----
    DataFrame columns are:
        SourceSystemIdentifier: A unique number or alphanumeric code assigned to a the update-comment by
            the source system
        SourceSystem: The system code or name providing the user data
        LMSUserIdentifier: A unique number or alphanumeric code assigned to a user by the source
            system
        LMSSectionIdentifier: A unique number or alphanumeric code assigned to a section by the
            source system
        ActivityDateTime: The date/time the replied was created.
        ActivityStatus: The status for the reply
        ActivityType: The type of activity: `Discussion reply`
        Content: The comment text.
        AssignmentIdentifier: A unique numeric identifier assigned to the assignment.
        ActivityTimeInMinutes: The total activity time in minutes.
        CreateDate: Date/time at which the record was first retrieved
        LastModifiedDate: Date/time when the record was modified, or when first retrieved
        SourceCreateDate: Date this record was created in the LMS
        SourceLastModifiedDate: Date this record was last updated in the LMS
    """
    # TODO: complete the mapping under ticket LMS-170
    return section_updates_df
