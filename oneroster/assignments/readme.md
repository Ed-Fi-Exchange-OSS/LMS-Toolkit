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

Quizzes are treated as assignments; the difference is that they are
automatically associated with a Google Form.

[Canvas Assignments](https://canvas.instructure.com/doc/api/assignments.html)

* `course_id`
* `id`
* `name`
* `description`
* `due_at` (contains both date & time)

[Quizzes](https://canvas.instructure.com/doc/api/quizzes.html) are a separate
construct that could be tracked.

[Schoology
Assignment](https://developers.schoology.com/api-documentation/rest-api-v1/assignment)

Each assignment is associated with a `section_id` when posting a new resources.
The concept of "assignment" is meant to encompass both coursework and
tests/quizzes.

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

## Activity Logging

Beyond the assignment submission status, are there other bits of activity data
that we can track for students?

* Google
  * Google Classroom does not appear to have anything useful built into it for
    tracking sign-in or discussions. [Confirmation in support
    forum](https://support.google.com/edu/classroom/thread/38716258?hl=en)
  * As noted above, quizzes are included in assignments.
* Canvas
  * Canvas has an [Authentications Log
    API](https://canvas.instructure.com/doc/api/authentications_log.html#method.authentication_audit_api.for_account)
    that tracks when a user logs in. User comments indicate that the session
    timeout is either 24 hrs or 48 hrs; this is configurable in the database
    apparently but not through the UI. So in a typical situation, a user's login
    activity would be seen once per day. That should be good enough for
    attendance tracking. But it could be once every two days, in which case
    there is a chance that a user would actually be using the system one day,
    but not show up in this authentication log on that day.
  * The [xAPI
    integration](https://canvas.instructure.com/doc/api/file.xapi.html) appears
    to be for _receiving_ data. It does mention: "This will update the activity
    time for the user in Canvas, and add a page view for that tool." Where is
    this activity time? And the Page resource doesn't have information on page
    views, so it is not clear what this statement really means. Maybe goes into
    the [course
    analytics](https://canvas.instructure.com/doc/api/analytics.html#method.analytics_api.course_participation).
  * Can also report on
    [Discussions](https://canvas.instructure.com/doc/api/discussion_topics.html).
    The URL requires you to query by course and topic to get a list of entries.
    The entries are associated with a `user_id`. This would require looping
    through the hierarchy. Entries and replies are separate entities, so need to
    look at both to see if a student is participating. Side note: relationship
    detection.
  * Quizzes are separate from assignments. Check out the [Quiz Submissions
    API](https://canvas.instructure.com/doc/api/quiz_submissions.html). Output includes:
    * `user_id`
    * `started_at`
    * `workflow_state`: untaken, pending_review, complete, settings_only, preview
  * The [Quiz Submissions Event
    API](https://canvas.instructure.com/doc/api/quiz_submission_events.html) is
    probably more fine-grained than we want, on the assumption that quizzes are
    generally timebound - that is, for our purposes, there is no need to see the
    individual details like entering or exiting a quiz page.
* Schoology
  * It is possible to query for
    [discussions](https://developers.schoology.com/api-documentation/rest-api-v1/discussion-thread)
    and [discussion
    replies](https://developers.schoology.com/api-documentation/rest-api-v1/discussion-reply).
    Both will return the `uid` (user id). The "Discussion" does not have a
    timestamp on it, but it does have a due date. So it appears to be a form of
    assignment, in which case only tracking the replies would be necessary.
  * Schoology has an [Attendance
    API](https://developers.schoology.com/api-documentation/rest-api-v1/attendance)
    that tracks present/absent/late/excused for an enrollment on a date. The
    [help
    shows](https://support.schoology.com/hc/en-us/articles/201001913-Courses-Attendance)
    that Course Admins track this manually. Wonder if K-12 schools are using
    this feature?

### Summary

* Google Classroom activity tracking is only through the course work submissions.
* Canvas and Schoology have reporting on discussion participation.
* Canvas distinguishes Quizzes from Assignments, thus should query for both to look for activity.
* Of the three, only Canvas has sign-in tracking. Due to long session time outs,
  a student could use the system on a day without needing to sign-in, and thus
  this is probably not a useful resource.
