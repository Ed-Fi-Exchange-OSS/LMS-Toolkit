"""
This script retrieves and writes out to CSV all students, sections, assignments,
and submissions for the desired grading period(s). Configuration is via `.env`
file or directly with environment variables:

* SCHOOLOGY_KEY=<administrator's API key>
* SCHOOLOGY_SECRET=<administrator's API secret>
* SCHOOLOGY_GRADING_PERIODS=<csv list of grading period ids>
"""

from datetime import datetime
import os
from prettyprinter import pprint

from dotenv import load_dotenv
import pandas as pd
import schoolopy
from schoolopy.models import Submission

class SchoologyExport:
    api_key = ''
    api_secret = ''
    desired_grading_periods = []
    grading_periods_lookup = {}
    output_path = ''
    sc_client = None

    def __init__(self):
        # TODO: find a better way. This value is set for Ed-Fi/MSDF users
        # because of an internal network issue. Necessary for running PIP. But
        # it messes with the commands below, so needs to be unset.
        os.environ["REQUESTS_CA_BUNDLE"] = ""

        self._get_configuration()
        self._initialize_connection()
        self._get_grading_periods()

    def _get_configuration(self):
        # TODO: long-term, probably want to allow values to be set at the command
        # line as alternate to environment variables.

        load_dotenv()

        ASSERT_TEMPLATE = '{key} environment variable is not set.'

        self.api_key = os.getenv('SCHOOLOGY_KEY')
        assert self.api_key is not None, ASSERT_TEMPLATE.format('SCHOOLOGY_KEY')

        self.api_secret = os.getenv('SCHOOLOGY_SECRET')
        assert self.api_secret is not None, ASSERT_TEMPLATE.format('SCHOOLOGY_SECRET')

        self.output_path = os.getenv('SCHOOLOGY_OUTPUT_PATH')
        assert self.api_secret is not None, ASSERT_TEMPLATE.format('SCHOOLOGY_OUTPUT_PATH')

        desired_grading_periods = os.getenv('SCHOOLOGY_GRADING_PERIODS')
        assert desired_grading_periods is not None, ASSERT_TEMPLATE.format('SCHOOLOGY_GRADING_PERIODS')

        try:
            self.desired_grading_periods = [int(gp) for gp in desired_grading_periods.split(',')]
        except ValueError as ex:
            msg = f'Grading period environment variable could not be parsed: {ex}'
            raise Exception(msg)

    def _initialize_connection(self):
        self.sc_client = schoolopy.Schoology(schoolopy.Auth(self.api_key, self.api_secret))

    def _get_grading_periods(self):
        gp_list = self.sc_client.get_grading_periods()
        gl = { gp.id : gp.title for gp in gp_list if gp.id in self.desired_grading_periods }
        self.grading_periods_lookup = gl

    def _create_file_name(self, base_name):
        if not os.path.exists(self.output_path):
            os.mkdir(self.output_path)

        file_name =  f'{base_name}.{datetime.now().strftime("%Y-%m-%d-%H-%M-%S")}.csv'
        return os.path.join(self.output_path, file_name)

    def _to_csv(self, data, base_name):
        df = pd.DataFrame(data = data)
        df.to_csv(self._create_file_name(base_name), mode = 'w', index = False)

    def _get_students(self):
        # Pull data from Schoology
        student_list = self.sc_client.get_students()

        # Reshape for our desired output
        def dto_to_student(student):
            return {
                'uid': student.uid,
                'school_id': student.school_id,
                'school_uid': student.school_uid,
                'name_first': student.name_first,
                'name_middle': student.name_middle,
                'name_last': student.name_last,
                'username': student.username,
                'email_address': student.primary_email
            }

        return [dto_to_student(s) for s in student_list]

    def _get_sections(self):
        # TODO: planning to build a fresh Schoology API package, at which time we
        # can delete the following extension method
        from schoolopy.models import Section
        def get_sections_for_course(Self):
            resource = "courses/{}/sections".format(Self.id)

            # TODO: make sure this handles situation where there are no sections for a course
            return [Section(raw) for raw in self.sc_client.get(resource)['section']]

        schoolopy.models.Course.get_sections = get_sections_for_course
        del get_sections_for_course
        # End extension

        # Pull data from Schoology
        course_list = self.sc_client.get_courses()

        section_list = []
        for c in course_list:
            # Filter only sections for the grading periods we care about.
            section_list += [c for c in c.get_sections()
                                for gp in self.grading_periods_lookup
                                if gp in c.grading_periods]

        # Reshape for our desired output
        def dto_to_section(section):
            return {
                'id': section.id,
                'course_id': section.course_id,
                'school_id': section.school_id,
                'course_title': section.course_title,
                'course_code': section.course_code,
                'section_title': section.section_title,
                'grading_period_ids': section.grading_periods,
                'grading_period_names': [self.grading_periods_lookup[gp] for gp in section.grading_periods],
                'enrollments': { e['id'] : e['uid'] for e in self.sc_client.get_enrollments(section.id) }
            }

        return [dto_to_section(s) for s in section_list]

    def _full_name(self, student):
        names = [student['name_first'], student['name_middle'], student['name_last']]
        return ' '.join(x for x in names if x)

    def _find_student(self, students, uid):
        return next(s for s in students if s['uid'] == uid)

    def _get_assignments(self, students, sections):
        def dto_to_assignment(section, assignment):
            a = {
                'id': assignment.id,
                'section_id': section['id'],
                'section_title': section['section_title'],
                'title': assignment.title,
                'due': assignment.due,
                'max_points': assignment.max_points,
                'is_final': assignment.is_final,
                'type': assignment.type,
                'grade_item_id': assignment.grade_item_id,
                'grading_period_id': assignment.grading_period,
                'grading_period_name': None,
                'assignee_ids': assignment.assignees,
                'assignee_names': []
            }

            if int(assignment.grading_period) in self.grading_periods_lookup:
                a['grading_period_name'] = self.grading_periods_lookup[int(assignment.grading_period)]

            if assignment.assignees:
                # Need to look up students vai the section['enrollments'], which
                # is of the form {section_id : student_uid}.
                enrollments = section['enrollments']
                assignees = [enrollments[str(i)] for i in assignment.assignees if str(i) in enrollments]
                a['assignee_names'] = [self._full_name(self._find_student(students, a)) for a in assignees]

            return a

        assignments = []
        for s in sections:
            # Pull from Schoology
            section_assigns = self.sc_client.get_assignments(s['id'])

            # Reshape for our desired output
            assignments += [dto_to_assignment(s, sa) for sa in section_assigns]

        return assignments

    def _get_submissions(self, students, assignments):
        def get_submissions(assignment):
            resource = f'sections/{assignment["section_id"]}/submissions/{assignment["grade_item_id"]}'

            # TODO: make sure this handles situation where there are no submissions
            return [Submission(raw) for raw in self.sc_client.get(resource)['revision']]

        def dto_to_submission(assignment, submission):
            s = {
                'section_id': assignment['section_id'],
                'section_title': assignment['section_title'],
                'assignment_id': assignment['id'],
                'assignment_title': assignment['title'],
                'revision_id': submission.revision_id,
                'student_uid': submission.uid,
                'student_name': self._full_name(self._find_student(students, str(submission.uid))),
                'created': datetime.fromtimestamp(submission.created),
                'late': submission.late,
                'draft': submission.draft
            }
            return s

        submissions = []
        for a in assignments:
            # Pull from Schoology
            section_subs = get_submissions(a)

            # Reshape for our desired output
            submissions += [dto_to_submission(a, sub) for sub in section_subs]

        return submissions

    def export_assignment_data(self):
        # se.students_to_csv()
        # se.sections_to_csv()

        students = self._get_students()
        self._to_csv(students, "students")

        sections = self._get_sections()
        self._to_csv(sections, "sections")

        assignments = self._get_assignments(students, sections)
        self._to_csv(assignments, "assignments")

        submissions = self._get_submissions(students, assignments)
        self._to_csv(submissions, "submissions")

if __name__ == '__main__':
    se = SchoologyExport()
    se.export_assignment_data()
