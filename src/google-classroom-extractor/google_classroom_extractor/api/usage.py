# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.

from datetime import datetime, timedelta
import logging
import os
from typing import List, Dict, Optional, Any, cast
from dateutil.parser import parse as date_parse
import pandas as pd  # type: ignore
from sqlalchemy.exc import OperationalError  # type: ignore
from sqlalchemy.engine.base import Engine as saEngine  # type: ignore
from googleapiclient.discovery import Resource  # type: ignore
from .api_caller import call_api, ResourceType


def request_usage(resource: Optional[Resource], date: str) -> List[Dict[str, str]]:
    assert isinstance(resource, Resource) or resource is None
    assert isinstance(date, str)

    if resource is None:
        return []

    return call_api(
        cast(ResourceType, resource).userUsageReport().get,
        {
            "userKey": "all",
            "date": date,
            "parameters": "classroom:timestamp_last_interaction,classroom:num_posts_created,accounts:timestamp_last_login",
        },
        "usageReports",
    )


def last_sync_date(sync_db: saEngine) -> Optional[datetime]:
    assert isinstance(sync_db, saEngine)

    with sync_db.connect() as con:
        try:
            usage_df = pd.read_sql("SELECT asOfDate FROM Usage", con)
            if usage_df["asOfDate"].count() == 0:
                return None
            return date_parse(usage_df["asOfDate"].max())
        except OperationalError:
            logging.debug("No Usage table yet")
            return None


def start_date(sync_db: saEngine) -> datetime:
    assert isinstance(sync_db, saEngine)

    last_date: Optional[datetime] = last_sync_date(sync_db)
    if last_date is not None:
        return last_date + timedelta(days=1)
    start_date_env = os.getenv("START_DATE")
    if start_date_env is None:
        return datetime.today()
    return date_parse(start_date_env)


def end_date() -> datetime:
    end_date_env = os.getenv("END_DATE")
    if end_date_env is None:
        return datetime.today()
    return date_parse(end_date_env)


def request_latest_usage_as_df(
    resource: Optional[Resource], start: datetime, end: datetime
) -> pd.DataFrame:
    assert isinstance(resource, Resource) or resource is None
    assert isinstance(start, datetime)
    assert isinstance(end, datetime)

    logging.info("Pulling usage data")

    if end < start:
        logging.warning("Usage data end time is before start time.")

    reports: List[Any] = []
    for date in pd.date_range(start=start, end=end):
        reports.extend(request_usage(resource, date.strftime("%Y-%m-%d")))

    usage: List[Dict[str, str]] = []
    for response in reports:
        row: Dict[str, str] = {}
        row["email"] = response.get("entity").get("userEmail")
        row["asOfDate"] = response.get("date")
        row["importDate"] = datetime.today().strftime("%Y-%m-%d")

        for parameter in response.get("parameters"):
            if parameter.get("name") == "classroom:num_posts_created":
                row["numberOfPosts"] = parameter.get("intValue")

            if parameter.get("name") == "classroom:last_interaction_time":
                row["lastInteractionTime"] = parameter.get("datetimeValue")

            if parameter.get("name") == "accounts:last_login_time":
                row["lastLoginTime"] = parameter.get("datetimeValue")
        usage.append(row)

    usage_df: pd.DataFrame = pd.json_normalize(usage)
    if usage_df.empty:
        return usage_df

    usage_df = usage_df.astype(
        {
            "email": "string",
            "asOfDate": "datetime64",
            "importDate": "datetime64",
            "numberOfPosts": "int32",
            "lastInteractionTime": "datetime64",
            "lastLoginTime": "datetime64",
        }
    )

    usage_df["name"] = usage_df["email"].str.split("@").str[0]
    usage_df["monthDay"] = usage_df["asOfDate"].dt.strftime("%m/%d")
    usage_df["nameDate"] = usage_df["name"] + " " + usage_df["monthDay"]

    return usage_df


def request_all_usage_as_df(
    resource: Optional[Resource], sync_db: saEngine
) -> pd.DataFrame:
    assert isinstance(resource, Resource) or resource is None
    assert isinstance(sync_db, saEngine)

    usage_df: pd.DataFrame = request_latest_usage_as_df(
        resource, start_date(sync_db), end_date()
    )
    if usage_df.empty:
        return usage_df

    usage_df.to_sql("Usage", sync_db, if_exists="append", index=False, chunksize=500)
    # remove duplicates - leave only the most recent
    with sync_db.connect() as con:
        con.execute(
            "DELETE from Usage "
            "WHERE rowid not in (select max(rowid) "
            "FROM Usage "
            "GROUP BY email, asOfDate)"
        )

    return usage_df
