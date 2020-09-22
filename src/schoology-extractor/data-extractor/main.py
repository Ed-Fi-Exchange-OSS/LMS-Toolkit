import os
from lib import export_data
from lib.users import Users
from lib.assignments import Assignments
from lib.sections import Sections
from lib.submissions import Submissions
from dotenv import load_dotenv

load_dotenv()
SCHOOLOGY_KEY = os.getenv("SCHOOLOGY_KEY")
SCHOOLOGY_SECRET = os.getenv("SCHOOLOGY_SECRET")
SCHOOLOGY_SECTION_IDS = os.getenv("SCHOOLOGY_SECTION_IDS")
SCHOOLOGY_OUTPUT_PATH = os.getenv("SCHOOLOGY_OUTPUT_PATH")

sections_id_array = SCHOOLOGY_SECTION_IDS.split(',')


# export users
users = Users(SCHOOLOGY_KEY, SCHOOLOGY_SECRET)

export_data.tocsv(users.get_all(), f"{SCHOOLOGY_OUTPUT_PATH}/users.csv")


# export sections
sections = Sections(SCHOOLOGY_KEY, SCHOOLOGY_SECRET)

sections_list = list()
for section_id in sections_id_array:
    sections_list.append(sections.get_by_id(section_id))

export_data.tocsv(sections_list,
                  f"{SCHOOLOGY_OUTPUT_PATH}/sections.csv")


# export assigments
assignments = Assignments(SCHOOLOGY_KEY, SCHOOLOGY_SECRET)

export_data.tocsv(assignments.get_by_section_id_array(sections_id_array),
                  f"{SCHOOLOGY_OUTPUT_PATH}/assignments.csv")


# export submissions
submissions = Submissions(SCHOOLOGY_KEY, SCHOOLOGY_SECRET)

submissions_list = list()
for section_id in sections_id_array:
    submissions_list.append(submissions.get_by_section_id(section_id))

export_data.tocsv(submissions_list,
                  f"{SCHOOLOGY_OUTPUT_PATH}/submissions.csv")
