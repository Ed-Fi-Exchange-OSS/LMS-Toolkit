# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.

from datetime import datetime, timedelta
import logging
from typing import List, Dict, Optional, Any, cast
from dateutil.parser import parse as date_parse
from pandas import DataFrame, json_normalize, read_sql, date_range
from sqlalchemy.exc import OperationalError
import sqlalchemy
from googleapiclient.discovery import Resource
from .api_caller import call_api, ResourceType

logger = logging.getLogger(__name__)


def request_usage(resource: Optional[Resource], date: str) -> List[Dict[str, str]]:

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


def last_sync_date(sync_db: sqlalchemy.engine.base.Engine) -> Optional[datetime]:
    with sync_db.connect() as con:
        try:
            usage_df = read_sql("SELECT asOfDate FROM Usage", con)
            if usage_df["asOfDate"].count() == 0:
                return None
            return date_parse(usage_df["asOfDate"].max())  # type: ignore
        except OperationalError:
            logger.debug("No Usage table yet")
            return None


def start_date(sync_db: sqlalchemy.engine.base.Engine, env_start_date: str) -> datetime:
    last_date: Optional[datetime] = last_sync_date(sync_db)
    if last_date is not None:
        return last_date + timedelta(days=1)
    if env_start_date == "":
        return datetime.today()
    return date_parse(env_start_date)


def end_date(env_end_date: str) -> datetime:
    if env_end_date == "":
        return datetime.today()
    return date_parse(env_end_date)


def request_latest_usage_as_df(
    resource: Optional[Resource], start: datetime, end: datetime
) -> DataFrame:
    logger.info("Pulling usage data")

    if end < start:
        logger.info("Usage data end time is before start time.")

    reports: List[Any] = []
    for date in date_range(start=start, end=end):
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

    usage_df: DataFrame = json_normalize(usage)
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
    resource: Optional[Resource],
    sync_db: sqlalchemy.engine.base.Engine,
    env_start_date: str,
    env_end_date: str,
) -> DataFrame:
    usage_df: DataFrame = request_latest_usage_as_df(
        resource, start_date(sync_db, env_start_date), end_date(env_end_date)
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
