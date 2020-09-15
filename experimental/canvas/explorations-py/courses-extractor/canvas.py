# This script uses the CanvasAPI to explore courses in the system, creating a
# CSV file as final output.
from canvasapi import Canvas
import os
import pprint
from collections import namedtuple
from datetime import datetime
from dotenv import load_dotenv
load_dotenv()

API_URL = os.getenv("CANVAS_BASE_URL")
API_KEY = os.getenv("CANVAS_ACCESS_TOKEN")
OUTPUT_URL = os.getenv("COURSES_EXTRACTOR_OUTPUT_PATH")

def flatten(pages):
    flat = []
    for p in pages:
        for p2 in p:
            flat.append(p2)
    return flat

def quote_string(value):
    if "\"" in value:
        value = value.replace("\"", "\\\"")
    if "," in value:
        value = "\"{}\"".format(value)
    return value

def get_course_for_csv(course):
    return [
        quote_string(course.name),
        str(course.id),
        str(course.start_at_date)
    ]

def main():
    canvas = Canvas(API_URL, API_KEY)

    # canvas.get_courses() returns only the courses that the current user is
    # enrolled in. To get all coureses in the system, need to first get accounts
    # that the current user can access.
    accounts = canvas.get_accounts()

    # This is a paginated list of accounts. We can get a paginated list of courses
    # for each account with account.get_courses(). Using list comprehension, create
    # a list of these course paginations:
    course_pages = [account.get_courses() for account in accounts]

    # This object is two-dimensional. Flatten it for ease of use.
    courses = flatten(course_pages)

    # Create a simple list of course names
    course_names = [course.name for course in courses]
    pprint.pprint(course_names)

    # Create a more complex list using a named tuple
    CCourse = namedtuple('CCourse', ['name', 'start_date', 'id'])
    complex_list = [CCourse(c.name, c.start_at_date, c.id) for c in courses]

    pprint.pprint(complex_list)

    # That was interesting, but I haven't figured out what to do with it other
    # than iterate over the list, which is not really an improvement on direct
    # access to the pages.
    records = [",".join([c.name, str(c.start_at_date)]) for c in courses]
    pprint.pprint(records)

    # That was better. Now let's quote those strings if they contain commas, and
    # wrap that in a function that extracts the desired attributes into an
    # array.
    records = [",".join(get_course_for_csv(c)) for c in courses]
    pprint.pprint(records)

    # Write out a file with datetime stamp in the name
    file_name = "canvas-courses-" + datetime.now().strftime("%Y-%m-%d-%H-%M-%S") + ".csv"
    with open(f"{OUTPUT_URL}/{file_name}", "w") as file:
        file.write("name,id,start_date\n")
        [file.write(r+"\n") for r in records]

if __name__ == "__main__":
	main()
