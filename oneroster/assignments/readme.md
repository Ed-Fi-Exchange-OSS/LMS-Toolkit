# Assignment Data

Goal: define some assignments that can be loaded into each LMS, along with
student submissions, so that we pull the same data from each LMS and wrangle
them into the same output format(s).

The following brief analysis of APIs assumes that we need very basic information
about assignments. There will likely be additional nuances that come up as we
begin exporting data and getting feedback from the community.

## Assignments

_Review of API and fields of interest_

[Google CourseWork
API](https://developers.google.com/classroom/reference/rest/v1/courses.courseWork#CourseWork)

* `courseId`
* `id`
* `title`
* `description`
* `dueDate`
* `dueTime`

[Canvas Assignments](https://canvas.instructure.com/doc/api/assignments.html)

* `course_id`
* `id`
* `name`
* `description`
* `due_at` (contains both date & time)

[Schoology
Assignment](https://developers.schoology.com/api-documentation/rest-api-v1/assignment)

Each assignment is associated with a `section_id` when posting a new resources.

* `title`
* `description`
* `due` (contains both date & time)

In summary, we can define an assignment via the following information.

* section or course or class id
* name or title
* description
* due date
* due time.

## Submission

What data do we need for a student's submission to an assignment? Note that wes
want to see if student has made progress, not just completed assignment, if
there is such a concept.

[Google StudentSubmissions API](https://developers.google.com/classroom/reference/rest/v1/courses.courseWork.studentSubmissions)

* `courseId`
* `courseWorkId`
* `userId`
* `creationTime`
* `updateTime`
* `state`: new (irrelevant to us?), created (in draft), turned_in (submitted), returned (graded)
* `late` (bool)
* `draftGrade`
* `assignedGrade`

[Canvas Submissions](https://canvas.instructure.com/doc/api/submissions.html)

* `assignmentId`
* `grade`
* `submitted_at`
* `user_id`
* `graded_at`
* `late_policy_status`: late, missing, none, or null
* `workflow_state`: submitted (or null for draft?)

[Schoology Submissions](https://developers.schoology.com/api-documentation/rest-api-v1/submissions)

Although the API is called "submissions", the resources seem to be "revisions".
They are submitted for "grade items". The `grade_item` property is also on
`assignment`, but it is not clear where this value comes from in the first
place. Wonder if
[Grade](https://developers.schoology.com/api-documentation/rest-api-v1/grade) is
what we really need here? The Assignments documentation states "Every assignment
has an entry in the gradebook." So three may be a grade record before a student
has submitted anything. In the end probably need both.

* Submissions
  * `created` (int - Unix timestamp)
  * `late` (int, presumably as bool 0/1)
  * `draft` (int as Boolean 0/1)
  * Associated with `section_id` and `grade_item_id` via the REST URL
* Grade
  * Grade
  * Type: assignment, discussion

In summary, we can define an assignment submission by the following information:

* Creation timestamp
* Clearly, must be associated with an assignment
* Is the assignment late?
* Status of submission: not started, draft, submitted, returned
* Grade
* Student

## Sample Data

Create two assignments per course:

1. One that is complete with all students submitting.
2. One that is in progress, with a mix of no submission, draft submission,
   completed submission, and returned (graded) submission.

Using the various APIs is feasible, but it would be simpler to login as each
student to complete the work. However, this means that we will not have control
over the submission dates. Need to think about this before committing. If
submitting assignments manually, we will need to adjust assignment due dates as
needed based on when we get access to a system so that due dates are not before
we could start adding submissions.

Easier approach: just make sure we can download the data. For improved
visualization can mock it up as needed for consistency without worrying about
the original data being exactly the same.
