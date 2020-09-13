import csv
import logging
import os
import sys
from faker import Faker

fake = Faker("en_US")

def random_id():
    return fake.random_number(digits=8)

def generate_courses(records):
    logging.info(f"Generating {records} course records")
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

    with open("courses.csv", "wt") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=headers)
        writer.writeheader()
        for i in range(1, records):
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


def generate_coursework(records):
    logging.info(f"Generating {records} coursework records")
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

    with open("coursework.csv", "wt") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=headers)
        writer.writeheader()
        for i in range(1, records):
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


INSTRUCTIONAL_DAYS_PER_SCHOOL_YEAR = 180
NUMBER_OF_COURSES = 500


def generate():
    logging.basicConfig(
        handlers=[
            logging.StreamHandler(sys.stdout),
        ],
        level=os.environ.get("LOGLEVEL", "INFO"),
    )

    generate_courses(NUMBER_OF_COURSES)
    generate_coursework(NUMBER_OF_COURSES * INSTRUCTIONAL_DAYS_PER_SCHOOL_YEAR)


if __name__ == "__main__":
    generate()
