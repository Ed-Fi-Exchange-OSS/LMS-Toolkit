# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.
from typing import List
from pandas import DataFrame
import pook
from pathlib import Path
from googleapiclient.discovery import build, Resource
from google.oauth2.service_account import Credentials
from google_classroom_extractor.api.resource_sync import (
    add_hash_and_json_to,
    add_sourceid_to,
)


def prep_expected_sync_df(df: DataFrame, identity_columns: List[str]) -> DataFrame:
    result_df: DataFrame = add_hash_and_json_to(df)
    add_sourceid_to(result_df, identity_columns)
    result_df = result_df[["Json", "Hash", "SourceId"]]
    result_df.set_index("SourceId", inplace=True)
    return result_df


def prep_from_sync_db_df(df: DataFrame, identity_columns: List[str]) -> DataFrame:
    result_df: DataFrame = df[["Json", "Hash", "SourceId"]]
    result_df.set_index("SourceId", inplace=True)
    return result_df


def setup_fake_reports_api(endpoint_suffix: str, response_json: str) -> Resource:
    """
    Set up a fake Google Reports SDK API using
    the pook HTTP traffic mocking library

    Parameters
    ----------
    endpoint_suffix: string
        is the suffix of the endpoint being faked,
        for example: "courses" for the courses endpoint
    response_json: string
        is the json response body to be returned

    Returns
    -------
    Resource
        a Google Reports SDK Resource

    Notes
    -----
    Requires pook to already be activated in a test
    """
    fake_discovery_endpoint_json: str = Path(
        "tests/api/fake-admin-discovery-endpoint.json"
    ).read_text()
    fake_credentials: Credentials = Credentials.from_service_account_file(
        "tests/api/fake-service-account.json", scopes=[], subject="x@example.com"
    )
    pook.get(
        "http://www.googleapis.com:443/discovery/v1/apis/admin/reports_v1/rest",
        response_json=fake_discovery_endpoint_json,
        reply=200,
    )
    pook.post(
        "http://oauth2.googleapis.com:443/token",
        response_json='{"access_token": "fake"}',
        reply=200,
    )
    pook.get(
        f"http://www.googleapis.com:443/admin/reports/v1/{endpoint_suffix}",
        response_json=response_json,
        reply=200,
    )
    return build(
        "admin", "reports_v1", credentials=fake_credentials, cache_discovery=False
    )


def setup_fake_classroom_api(endpoint_suffix: str, response_json: str) -> Resource:
    """
    Set up a fake Google Classroom/Admin SDK API using
    the pook HTTP traffic mocking library

    Parameters
    ----------
    endpoint_suffix: string
        is the suffix of the endpoint being faked,
        for example: "courses" for the courses endpoint
    response_json: string
        is the json response body to be returned

    Returns
    -------
    Resource
        a Google Classroom SDK Resource

    Notes
    -----
    Requires pook to already be activated in a test
    """
    fake_discovery_endpoint_json: str = Path(
        "tests/api/fake-classroom-discovery-endpoint.json"
    ).read_text()
    fake_credentials: Credentials = Credentials.from_service_account_file(
        "tests/api/fake-service-account.json", scopes=[], subject="x@example.com"
    )
    pook.get(
        "http://www.googleapis.com:443/discovery/v1/apis/classroom/v1/rest",
        response_json=fake_discovery_endpoint_json,
        reply=200,
    )
    pook.post(
        "http://oauth2.googleapis.com:443/token",
        response_json='{"access_token": "fake"}',
        reply=200,
    )
    pook.get(
        f"http://classroom.googleapis.com:443/v1/{endpoint_suffix}",
        response_json=response_json,
        reply=200,
    )
    return build("classroom", "v1", credentials=fake_credentials, cache_discovery=False)
