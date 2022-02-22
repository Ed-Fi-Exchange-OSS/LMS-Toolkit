# Explore the API using https://edfialliance.instructure.com/graphiql

import os
import json
import timeit
from typing import Optional

from dotenv import load_dotenv
import pandas as pd

# There may some useful GraphQL-specific libraries out there. Didn't
# investigate - just wanted to keep this spike very elementary.
import requests

ACCOUNT_ID = 1
# Canvas says: "Request reasonable page sizes to avoid being limited." what is
# that supposed to mean? We would need to explore this more and compare with
# page size we're using in the normal REST query. Starting with a small page
# size to test out the functionality.

# Existing code uses canvasapi library, which sets page size to 100.
PAGE_SIZE = 100

load_dotenv()
canvas_token = os.getenv("CANVAS_TOKEN")
canvas_base_url = os.getenv("CANVAS_BASE_URL")

start_time = timeit.default_timer()


def build_course_query(after_cursor: Optional[str] = "") -> str:
    return f"""
query MyQuery {{
  account(id: {ACCOUNT_ID}) {{
    coursesConnection(
        first: {PAGE_SIZE}
        after: "{after_cursor}"
      ) {{
      pageInfo {{
        hasNextPage
        endCursor
      }}
      nodes {{
        _id
        name
        state
        sisId
        enrollmentsConnection {{
          nodes {{
            user {{
              _id
              email
              name
              sisId
            }}
            _id
            state
            type
            section {{
              _id
            }}
          }}
        }}
      }}
    }}
  }}
}}
"""


url = f"{canvas_base_url}/api/graphql"
headers = {"Authorization": f"Bearer {canvas_token}"}


def post(query: str):
    r = requests.post(url, headers=headers, json={"query": query})

    if not r.status_code == 200:
        r.raise_for_status()

    body = json.loads(r.text)

    if "errors" in body:
        raise RuntimeError(str(body))

    # This should be a callback / Callable, not hard-coded
    process_course_query(body)


courses = []
students = []
enrollments = []
courses_end_cursor = ""


def process_course_query(body: dict) -> None:
    course_connections = body["data"]["account"]["coursesConnection"]

    for course_j in course_connections["nodes"]:
        # Note: Graphql courses returns deleted courses, and there is no obvious
        # way to filter in the query. We really don't want those.
        if course_j["state"] == "deleted":
            continue

        courses.append(
            {
                "CourseName": course_j["name"],
                "SourceSystemIdentifier": course_j["_id"],
            }
        )

        enrollment_connections = course_j["enrollmentsConnection"]
        for enroll_j in enrollment_connections["nodes"]:
            # Skip teachers. There's probably a "where clause" that could be
            # added to the GraphQL query, but didn't look it up.
            # For comparison between call types, just get all enrollments
            #
            # TYPE_TEACHER = "TeacherEnrollment"
            # TYPE_STUDENT = "StudentEnrollment"
            # if enroll_j["node"]["type"] == TYPE_TEACHER:
            #     continue

            # Regular API calls default to returning only students in the
            # "active" and "invited" states.
            # https://canvas.instructure.com/doc/api/enrollments.html GraphQL
            # doesn't provide that. For best comparison of results, manually
            # filter on those.
            if enroll_j["state"] not in ("active", "invited"):
                continue

            user_j = enroll_j["user"]
            students.append(
                {
                    "Email": user_j["email"],
                    "SisIdentifier": user_j["sisId"],
                    "StudentName": user_j["name"],
                    "SourceSystemIdentifier": user_j["_id"],
                }
            )

            enrollments.append(
                {
                    "SectionSourceSystemIdentifier": enroll_j["section"]["_id"],
                    "StudentSourceSystemIdentifier": user_j["_id"],
                    "SourceSystemIdentifier": enroll_j["_id"],
                }
            )

            # TODO: handle enrollment paging. No idea how to do that right now. Nested paging?

    # Course-level paging
    course_page = course_connections["pageInfo"]
    if course_page["hasNextPage"] == True:
        after = course_page["endCursor"]
        query = build_course_query(after)

        # Recursive call. This code is quick-and-dirty. Not thinking
        # very carefully about state and output. Just get it done.
        post(query)


post(build_course_query())

courses_df = pd.DataFrame(courses)
courses_df.astype({"SourceSystemIdentifier": int})
courses_df.sort_values(by=["SourceSystemIdentifier"], inplace=True)
courses_df.to_csv("courses.csv", index=False)

enrollments_df = pd.DataFrame(enrollments)
enrollments_df.astype({"SourceSystemIdentifier": int})
enrollments_df.sort_values(by=["SourceSystemIdentifier"], inplace=True)
enrollments_df.to_csv("enrollments.csv", index=False)

# In this quick-and-dirty, students enrolled in multiple classes will have
# multiple records. Real solution should de-duplicate.
students_df = pd.DataFrame(students)
students_df.astype({"SourceSystemIdentifier": int})
students_df.sort_values(by=["SourceSystemIdentifier"], inplace=True)
students_df.to_csv("students.csv", index=False)

elapsed = timeit.default_timer() - start_time

print(f"Elapsed time: {elapsed}")

# Run 1: 11 s
# Run 2: 7 s
# Run 3: 7 s
# Run 4: 7 s
# Run 5: 6 s
# Avg: 7 s

# Always takes longer first execution. Probably caching some results. So first execution counts for more.
