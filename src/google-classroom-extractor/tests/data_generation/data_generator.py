# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.

import csv
import logging
import os
import sys
from faker import Faker

fake = Faker("en_US")


def random_id():
    return fake.random_number(digits=8)


def generate_usage(record_count):
    logging.info(f"Generating {record_count} usage records")
    headers = [
        "email",
        "asOfDate",
        "importDate",
        "numberOfPosts",
        "lastInteractionTime",
        "lastLoginTime",
        "name",
        "monthDay",
        "nameDate",
    ]

    with open("generated-usage.csv", "wt") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=headers)
        writer.writeheader()
        for i in range(1, record_count):
            if i % 1000 == 0:
                logging.info(f"{i} records...")
            name = fake.name().lower().replace(" ", ".")
            writer.writerow(
                {
                    "email": fake.email(),
                    "asOfDate": fake.date_time_this_month(),
                    "importDate": fake.date_time_this_month(),
                    "numberOfPosts": fake.random_number(digits=1),
                    "lastInteractionTime": fake.date_time_this_month(),
                    "lastLoginTime": fake.date_time_this_month(),
                    "name": name,
                    "monthDay": "08/20",
                    "nameDate": f"{name} 08/20",
                }
            )


def generate_courses(record_count):
    logging.info(f"Generating {record_count} course records")
    headers = [
        "id",
        "name",
        "section",
        "descriptionHeading",
        "description",
        "room",
        "ownerId",
        "creationTime",
        "updateTime",
        "enrollmentCode",
        "courseState",
        "alternateLink",
        "teacherGroupEmail",
        "courseGroupEmail",
        "guardiansEnabled",
        "calendarId",
    ]

    with open("generated-courses.csv", "wt") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=headers)
        writer.writeheader()
        for i in range(1, record_count):
            if i % 1000 == 0:
                logging.info(f"{i} records...")
            writer.writerow(
                {
                    "id": random_id(),
                    "name": fake.name(),
                    "section": fake.random_number(digits=2),
                    "descriptionHeading": fake.catch_phrase(),
                    "description": fake.sentence(),
                    "room": fake.bothify("?###"),
                    "ownerId": random_id(),
                    "creationTime": fake.date_time_this_year(),
                    "updateTime": fake.date_time_this_month(),
                    "enrollmentCode": fake.random_number(digits=6),
                    "courseState": "ACTIVE",
                    "alternateLink": fake.uri(),
                    "teacherGroupEmail": fake.email(),
                    "courseGroupEmail": fake.email(),
                    "guardiansEnabled": True,
                    "calendarId": random_id(),
                }
            )


def generate_coursework(record_count):
    logging.info(f"Generating {record_count} coursework records")
    headers = [
        "courseId",
        "id",
        "title",
        "description",
        "state",
        "creationTime",
        "updateTime",
        "dueDate",
        "dueTime",
        "scheduledTime",
        "maxPoints",
        "workType",
        "creatorUserId",
        "topicId",
    ]

    with open("generated-coursework.csv", "wt") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=headers)
        writer.writeheader()
        for i in range(1, record_count):
            if i % 1000 == 0:
                logging.info(f"{i} records...")
            writer.writerow(
                {
                    "courseId": random_id(),
                    "id": random_id(),
                    "title": fake.catch_phrase(),
                    "description": fake.sentence(),
                    "state": "PUBLISHED",
                    "creationTime": fake.date_time_this_year(),
                    "updateTime": fake.date_time_this_month(),
                    "dueDate": fake.date_this_month(),
                    "dueTime": fake.time(),
                    "scheduledTime": fake.time(),
                    "maxPoints": fake.random_number(digits=2),
                    "workType": "ASSIGNMENT",
                    "creatorUserId": random_id(),
                    "topicId": random_id(),
                }
            )


def generate_students(record_count):
    logging.info(f"Generating {record_count} student records")
    headers = [
        "courseId",
        "userId",
        "profile.id",
        "profile.name.givenName",
        "profile.name.familyName",
        "profile.name.fullName",
        "profile.emailAddress",
    ]

    with open("generated-students.csv", "wt") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=headers)
        writer.writeheader()
        for i in range(1, record_count):
            if i % 1000 == 0:
                logging.info(f"{i} records...")
            given_name = fake.first_name()
            family_name = fake.last_name()
            full_name = f"{given_name} {family_name}"
            writer.writerow(
                {
                    "courseId": random_id(),
                    "userId": random_id(),
                    "profile.id":  random_id(),
                    "profile.name.givenName": given_name,
                    "profile.name.familyName": family_name,
                    "profile.name.fullName": full_name,
                    "profile.emailAddress": fake.email(),
                }
            )


def generate_submissions(record_count):
    logging.info(f"Generating {record_count} submission records")
    headers = [
        "courseId",
        "courseWorkId",
        "id",
        "userId",
        "creationTime",
        "updateTime",
        "state",
        "draftGrade",
        "assignedGrade",
        "courseWorkType",
    ]

    with open("generated-submissions.csv", "wt") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=headers)
        writer.writeheader()
        for i in range(1, record_count):
            if i % 1000 == 0:
                logging.info(f"{i} records...")
            writer.writerow(
                {
                    "courseId": random_id(),
                    "courseWorkId": random_id(),
                    "id": random_id(),
                    "userId": random_id(),
                    "creationTime": fake.date_time_this_year(),
                    "updateTime": fake.date_time_this_month(),
                    "state": "CREATED",
                    "draftGrade": fake.random_number(digits=2),
                    "assignedGrade": fake.random_number(digits=2),
                    "courseWorkType": "ASSIGNMENT",
                }
            )


INSTRUCTIONAL_DAYS_PER_SCHOOL_YEAR = 180
NUMBER_OF_COURSES = 500
NUMBER_OF_STUDENTS = 50000
NUMBER_OF_COURSEWORKS = NUMBER_OF_COURSES * INSTRUCTIONAL_DAYS_PER_SCHOOL_YEAR


def generate():
    logging.basicConfig(
        handlers=[
            logging.StreamHandler(sys.stdout),
        ],
        level=os.environ.get("LOGLEVEL", "INFO"),
    )

    generate_students(100)
    generate_courses(100)
    generate_coursework(100)
    generate_submissions(100)

    # generate_students(NUMBER_OF_STUDENTS)
    # generate_courses(NUMBER_OF_COURSES)
    # generate_coursework(NUMBER_OF_COURSEWORKS)
    # generate_submissions(NUMBER_OF_COURSEWORKS)  # times number of students

    generate_usage(100)


if __name__ == "__main__":
    generate()
