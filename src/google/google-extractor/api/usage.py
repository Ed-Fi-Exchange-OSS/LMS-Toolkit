import logging
import os
from datetime import datetime
import pandas as pd
from .api_caller import call_api


def request_usage(resource, date):
    return call_api(
        resource.userUsageReport().get,
        {
            "userKey": "all",
            "date": date,
            "parameters": "classroom:timestamp_last_interaction,classroom:num_posts_created,accounts:timestamp_last_login",
        },
        "usageReports",
    )


def usage_dataframe(resource):
    logging.info("Pulling usage data")
    reports = []
    # pylint: disable=no-member
    for date in pd.date_range(
        start=os.getenv("START_DATE"), end=os.getenv("END_DATE")
    ).strftime("%Y-%m-%d"):
        reports.extend(request_usage(resource, date))

    usage = []
    for response in reports:
        row = {}
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

    usage_df = pd.json_normalize(usage).astype(
        {
            "email": "string",
            "asOfDate": "datetime64",
            "importDate": "datetime64",
            "numberOfPosts": "int32",
            "lastInteractionTime": "datetime64",
            "lastLoginTime": "datetime64",
        }
    )

    # TODO: get this from a join with student profile
    usage_df["name"] = usage_df["email"].str.split("@").str[0]

    usage_df["monthDay"] = usage_df["asOfDate"].dt.strftime("%m/%d")
    usage_df["nameDate"] = usage_df["name"] + " " + usage_df["monthDay"]
    return usage_df
