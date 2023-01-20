# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.

import json
import logging
import requests
from datetime import datetime, timezone

from typing import Dict, List, Optional
from opnieuw import retry

from edfi_canvas_extractor.config import RETRY_CONFIG

from .canvas_helper import remove_duplicates
from .schema import query_builder
from .utils import validate_date, format_full_date


class GraphQLExtractor(object):
    assignments: List
    courses: List
    enrollments: List
    sections: List
    submissions: List
    students: List

    def __init__(
        self,
        url: str,
        token: str,
        account: str,
        start: Optional[str],
        end: Optional[str]
    ):
        """
        Initialize Adapter for GraphQL Extraction

        Parameters
        -----------
        url: str
            Base URL to connect to Canvas
        token: str
            Secret to get access to Canvas
        """
        self.assignments = list()
        self.courses = list()
        self.has_data = False
        self.enrollments = list()
        self.sections = list()
        self.submissions = list()
        self.students = list()

        self.set_account(account)
        self.set_credentials(url, token)
        self.set_dates(start, end)

    @retry(**RETRY_CONFIG)  # type: ignore
    def get_from_canvas(self, query: str):
        """
        Get GraphQL Query from Canvas

        Parameters
        ----------
        query: str
            query string for GraphQL

        Returns
        -------
        Dict JSON Object
        """

        GRAPHQL_URL = f"{self.url}/api/graphql"
        GRAPHQL_AUTH = {'Authorization': f'Bearer {self.token}'}

        fetch = requests.post(
            GRAPHQL_URL,
            headers=GRAPHQL_AUTH,
            json={"query": query}
            )
        if fetch.status_code != 200:
            fetch.raise_for_status()

        body = json.loads(fetch.text)

        if "errors" in body:
            raise RuntimeError(str(body))
        return body

    def extract(self, body) -> None:
        """
        Extract data from GraphQL query in Canvas

        Parameters
        ----------
        body: Dict JSON Object
        """
        courses = body["data"]["account"]["coursesConnection"]["nodes"][0]

        for course in courses["term"]["coursesConnection"]["nodes"]:
            if course["state"] not in ["available", "completed"]:
                continue

            start_term = courses["term"]["startAt"]
            end_term = courses["term"]["endAt"]

            if start_term is not None and end_term is not None:
                if not validate_date(self.start, self.end, start_term, end_term):
                    continue

            self.courses.append({
                "id": course["_id"],
                "name": course["name"],
                "state": course["state"],
                })

            sections = course["sectionsConnection"]["nodes"]
            for section in sections:
                self.sections.append({
                    "id": section["_id"],
                    "name": section["name"],
                    "course_id": course["_id"],
                    "sis_section_id": section["sisId"],
                    "created_at": section["createdAt"],
                    "updated_at": section["updatedAt"],
                    })

            enrollments = course["enrollmentsConnection"]
            student_associations = list()
            for enrollment in enrollments["nodes"]:
                if enrollment["state"] in ["active", "invited"] and enrollment["type"] == "StudentEnrollment":
                    users = enrollment["user"]

                    self.students.append({
                        "id": users["_id"],
                        "sis_user_id": users["sisId"],
                        "created_at": users["createdAt"],
                        "name": users["name"],
                        "email": users["email"],
                        "login_id": users["loginId"],
                    })

                    enrollment_dict = {
                        "id": enrollment["_id"],
                        "user_id": users["_id"],
                        "course_section_id": enrollment["section"]["_id"],
                        "enrollment_state": enrollment["state"],
                        "type": enrollment["type"],
                        "created_at": enrollment["createdAt"],
                        "updated_at": enrollment["updatedAt"],
                        }

                    if enrollment.get("grades"):
                        grades = {
                            "final_score": enrollment["grades"]["finalScore"],
                            "final_grade": enrollment["grades"]["finalGrade"],
                            "current_score": enrollment["grades"]["currentScore"],
                            "current_grade": enrollment["grades"]["currentGrade"],
                        }
                        enrollment_dict["grades"] = grades

                    student_associations.append(enrollment_dict)
                    self.enrollments.append(enrollment_dict)

            assignments = list()
            if course.get("assignmentsConnection", {}).get("nodes"):
                assignments = course["assignmentsConnection"]["nodes"]
                for assignment in assignments:
                    self.assignments.append({
                        "id": assignment["_id"],
                        "name": assignment["name"],
                        "description": assignment["description"],
                        "created_at": assignment["createdAt"],
                        "updated_at": assignment["updatedAt"],
                        "lock_at": assignment["lockAt"],
                        "unlock_at": assignment["unlockAt"],
                        "due_at": assignment["dueAt"],
                        "submission_types": assignment["submissionTypes"],
                        "course_id": course["_id"],
                        "points_possible": assignment["pointsPossible"],
                    })

            if course.get("submissionsConnection", {}).get("nodes"):
                # Get the section
                _section_ids = [_section["_id"] for _section in sections]
                # For each section with submissions
                for _section_id in _section_ids:
                    logging.debug(f"Section > {_section_id}")
                    # Get the assignments
                    for _assignment in course.get("assignmentsConnection", {}).get("nodes"):
                        assignment_id = _assignment["_id"]

                        is_past_due = False
                        now = datetime.now(timezone.utc)

                        if _assignment["dueAt"] is not None:
                            due_date = format_full_date(_assignment["dueAt"])
                            is_past_due = (due_date - now).days <= 0

                        logging.debug(f"Assignment > {assignment_id}")
                        # Get the enrollments in the section
                        _enrolled_users = [
                            _enrollment["user"]["_id"]
                            for _enrollment
                            in course.get("enrollmentsConnection", {}).get("nodes")
                            if _enrollment["section"]["_id"] == _section_id
                            if _enrollment["type"] not in ["TeacherEnrollment"]
                            ]
                        logging.debug("Enrollments of the section")
                        logging.debug(json.dumps(_enrolled_users, indent=2))
                        for _enrollment in _enrolled_users:
                            logging.debug(f"Enrollment > {_enrollment}")
                            _submission = [
                                _submission
                                for _submission
                                in course.get("submissionsConnection", {}).get("nodes")
                                if _submission["user"]["_id"] == _enrollment
                                if _submission["assignment"]["_id"] == assignment_id
                                ]
                            if _submission:
                                logging.debug(f"There is a submission for {_enrollment} in assignment {assignment_id}")
                                submission = _submission[0]
                                _new_submission = {
                                    "course_id": course["_id"],
                                    "section_id": _section_id,
                                    "assignment_id": submission["assignment"]["_id"],
                                    "id": submission["_id"],
                                    "user_id": submission["user"]["_id"],
                                    "late": submission["late"],
                                    "missing": submission["missing"],
                                    "submitted_at": submission["submittedAt"],
                                    "grade": submission["grade"],
                                    "created_at": submission["createdAt"],
                                    "updated_at": submission["updatedAt"],
                                    "graded_at": submission["gradedAt"],
                                    }
                                self.submissions.append(_new_submission)
                            else:
                                logging.debug(f"There are no submissions for {_enrollment} in assignment {assignment_id}")
                                _no_submission = {
                                    "course_id": course["_id"],
                                    "section_id": _section_id,
                                    "assignment_id": assignment_id,
                                    "id": f"{_section_id}#{assignment_id}#{_enrollment}",
                                    "user_id": _enrollment,
                                    "late": False,
                                    "missing": is_past_due,
                                    "submitted_at": None,
                                    "grade": None,
                                    "created_at": None,
                                    "updated_at": None,
                                    "graded_at": None,
                                }
                                self.submissions.append(_no_submission)
            else:
                for _assignment in assignments:
                    assignment_id = _assignment["_id"]
                    logging.debug(f"There are no submissions for assignment {assignment_id}")

                    is_past_due = False
                    now = datetime.now(timezone.utc)

                    if _assignment["dueAt"] is not None:
                        due_date = format_full_date(_assignment["dueAt"])
                        is_past_due = (due_date - now).days <= 0

                    for _enrolled in student_associations:
                        _section_id = _enrolled["course_section_id"]
                        _user_id = _enrolled["user_id"]

                        _no_submission = {
                            "course_id": course["_id"],
                            "section_id": _section_id ,
                            "assignment_id": assignment_id,
                            "id": f"{_section_id}#{assignment_id}#{_user_id}",
                            "user_id": _user_id,
                            "late": False,
                            "missing": is_past_due,
                            "submitted_at": None,
                            "grade": None,
                            "created_at": None,
                            "updated_at": None,
                            "graded_at": None,
                        }
                        self.submissions.append(_no_submission)

            if courses.get("pageInfo"):
                courses_page = courses["pageInfo"]
                if courses_page["hasNextPage"]:
                    after = courses_page["endCursor"]
                    query = query_builder(self.account, after)
                    self.get_from_canvas(query)

    def get_assignments(self) -> List[Dict[str, str]]:
        """
        Returns a sorted List of Assignments
        Returns
        -------
        List[Dict[str, str]]
            a List of Assignments
        """
        assignments = self.assignments
        return sorted(assignments, key=lambda x: x["id"])

    def get_courses(self) -> List:
        """
        Returns a List of Courses

        Returns
        -------
        List
            a List of Courses
        """
        return self.courses

    def get_enrollments(self) -> List:
        """
        Returns a sorted List of Enrollments

        Returns
        -------
        List
            a List of Enrollments
        """
        enrollments = self.enrollments
        return sorted(enrollments, key=lambda x: x["course_section_id"])

    def get_sections(self) -> List:
        """
        Returns a sorted List of Sections

        Returns
        -------
        List
            a List of Sections
        """
        sections = self.sections
        return sorted(sections, key=lambda x: x["id"])

    def get_submissions(self) -> List:
        """
        Returns a sorted List of Submissions
        Returns
        -------
        List
            a List of Submissions
        """
        submissions = self.submissions
        return sorted(submissions, key=lambda x: x["section_id"])

    def get_students(self) -> List:
        """
        Returns a sorted List of Students

        Returns
        -------
        List
            a List of Students
        """
        students = remove_duplicates(self.students, "id")
        return sorted(students, key=lambda x: x["id"])

    def set_account(self, account) -> None:
        """
        Set account number to get from GraphQL

        Parameters
        ----------
        account: str
            an account number
        """
        self.account = account

    def set_credentials(self, url: str, token: str) -> None:
        """
        Set credentials to get from GraphQL

        Parameters
        ----------
        args: MainArguments
        """
        self.url = url
        self.token = token

    def set_dates(self, start, end) -> None:
        """
        Set dates to filter courses fetched from
        GraphQL query in Canvas

        Parameters
        ----------
        start: str
            a string with start date
        end: str
            a string with end date
        """
        self.start = start
        self.end = end

    def run(self) -> None:
        """
        Builds and executes a GraphQL query, storing the results in self for
        further processing.
        """
        if not self.has_data:
            query = query_builder(self.account)

            data = self.get_from_canvas(query)

            if data:
                self.extract(data)
                self.has_data = True
        return None
