import os
import timeit

from dotenv import load_dotenv
import pandas as pd
from canvasapi import Canvas

ACCOUNT_ID = 1

load_dotenv()
canvas_token = os.getenv("CANVAS_TOKEN")
canvas_base_url = os.getenv("CANVAS_BASE_URL")

start_time = timeit.default_timer()

canvas = Canvas(canvas_base_url, canvas_token)

courses = []
enrollments = []
students = []
account = canvas.get_account(1)

for course_api in [c for c in account.get_courses()]:

    courses.append(
        {"CourseName": course_api.name, "SourceSystemIdentifier": course_api.id}
    )

    # Like graphql, go ahead and let it retrieve teachers
    enrollments_api = [u for u in course_api.get_enrollments()]
    enrollments.extend(
        [
            {
                "SectionSourceSystemIdentifier": u.course_section_id,
                "StudentSourceSystemIdentifier": u.user_id,
                "SourceSystemIdentifier": u.id,
            }
            for u in enrollments_api
        ]
    )
    students_api = [u for u in course_api.get_users()]
    students.extend(
        [
            {
                "Email": u.email,
                "SisIdentifier": u.sis_user_id,
                "StudentName": u.name,
                "SourceSystemIdentifier": u.id,
            }
            for u in students_api
        ]
    )


courses_df = pd.DataFrame(courses)
courses_df.astype({"SourceSystemIdentifier": int})
courses_df.sort_values(by=["SourceSystemIdentifier"], inplace=True)
courses_df.to_csv("courses_api.csv", index=False)

enrollments_df = pd.DataFrame(enrollments)
enrollments_df.astype({"SourceSystemIdentifier": int})
enrollments_df.sort_values(by=["SourceSystemIdentifier"], inplace=True)
enrollments_df.to_csv("enrollments_api.csv", index=False)

# In this quick-and-dirty, students enrolled in multiple classes will have
# multiple records. Real solution should de-duplicate.
students_df = pd.DataFrame(students)
students_df.astype({"SourceSystemIdentifier": int})
students_df.sort_values(by=["SourceSystemIdentifier"], inplace=True)
students_df.to_csv("students_api.csv", index=False)

elapsed = timeit.default_timer() - start_time

print(f"Elapsed time: {elapsed}")


# Run 1: 91 s
# Run 2: 88 s
# Run 3: 95 s
# Run 4: 90 s
# Run 5: 89 s
# Avg: 91 s
