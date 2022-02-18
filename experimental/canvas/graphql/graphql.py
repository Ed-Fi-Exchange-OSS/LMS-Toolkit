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
# Canvas says: "Request reasonable page sizes to avoid being limited."
# what is that supposed to mean? We would need to explore this more
# and compare with page size we're using in the normal REST query.
# Starting with a small page size to test out the functionality.
PAGE_SIZE = 10

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
      edges {{
        node {{
          _id
          name
          enrollmentsConnection {{
            edges {{
              node {{
                user {{
                  _id
                  email
                  name
                  sisId
                }}
                _id
                type
              }}
            }}
          }}
        }}
      }}
      pageInfo {{
        hasNextPage
        endCursor
      }}
    }}
  }}
}}
"""

url = f"{canvas_base_url}/api/graphql"
headers = { "Authorization": f"Bearer {canvas_token}" }

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
students = [] # review details - does this include teachers?
enrollments = []
courses_end_cursor = ""

def process_course_query(body: dict) -> None:
    course_connections = body["data"]["account"]["coursesConnection"]

    for course_j in course_connections["edges"]:
        courses.append({
            # TODO: check on actual UDM properties
            "CourseName": course_j["node"]["name"],
            "SourceSystemIdentifier": course_j["node"]["_id"],
        })

        enrollment_connections = course_j["node"]["enrollmentsConnection"]
        for enroll_j in enrollment_connections["edges"]:
            # Skip teachers
            TYPE_TEACHER = "TeacherEnrollment"
            # TYPE_STUDENT = "StudentEnrollment"
            if enroll_j["node"]["type"] == TYPE_TEACHER:
                continue

            user_j = enroll_j["node"]["user"]
            students.append({
                "Email": user_j["email"],
                "SisIdentifier": user_j["sisId"],
                "StudentName": user_j["name"],
                "SourceSystemIdentifier": user_j["_id"]
            })

            enrollments.append({
                "CourseSourceSystemIdentifier": course_j["node"]["_id"],
                "StudentSourceSystemIdentifier": user_j["_id"],
                "SourceSystemIdentifier": enroll_j["node"]["_id"]
            })

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
courses_df.to_csv("courses.csv")

enrollments_df = pd.DataFrame(enrollments)
enrollments_df.to_csv("enrollments.csv")

students_df = pd.DataFrame(students)
students_df.to_csv("students.csv")

elapsed = timeit.default_timer() - start_time

print(f"Elapsed time: {elapsed}")
