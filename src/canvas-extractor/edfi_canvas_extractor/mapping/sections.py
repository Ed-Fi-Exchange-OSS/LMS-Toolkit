# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.

import pandas as pd
from pandas import DataFrame

from . import constants


def map_to_udm_sections(sections_df: pd.DataFrame) -> pd.DataFrame:
    """
    Maps a DataFrame containing Canvas sections into the Ed-Fi LMS Unified Data
    Model (UDM) format.

    Parameters
    ----------
    sections_df: DataFrame
        Pandas DataFrame containing all Canvas sections

    Returns
    -------
    DataFrame
        A LMSSections-formatted DataFrame

    Notes
    -----
    DataFrame columns are:
        LMSSectionStatus: The section status from the source system
        SISSectionIdentifier: The section identifier defined in the Student Information System
        SectionDescription: The section description
        SourceSystem: The system code or name providing the section data
        SourceSystemIdentifier: A unique number or alphanumeric code assigned to a section
            by the source system
        Term: The enrollment term for the section
        Title: The section title or name
        SourceCreateDate: Date this record was created in the LMS
        SourceLastModifiedDate: Date this record was last updated in the LMS
        CreateDate: Date this record was created in the extractor
        LastModifiedDate: Date this record was last updated in the extractor
    """

    if sections_df.empty:
        return sections_df

    assert "id" in sections_df.columns
    assert "name" in sections_df.columns
    assert "sis_section_id" in sections_df.columns
    assert "CreateDate" in sections_df.columns
    assert "LastModifiedDate" in sections_df.columns

    df: DataFrame = sections_df[
        [
            "id",
            "name",
            "sis_section_id",
            "CreateDate",
            "LastModifiedDate",
        ]
    ].copy()

    df.rename(
        columns={
            "id": "SourceSystemIdentifier",
            "sis_section_id": "SISSectionIdentifier",
            "name": "Title",
        },
        inplace=True,
    )

    df["Term"] = ""
    df["SectionDescription"] = ""
    df["SourceSystem"] = constants.SOURCE_SYSTEM
    df["LMSSectionStatus"] = ""
    df["SourceCreateDate"] = ""
    df["SourceLastModifiedDate"] = ""

    return df
