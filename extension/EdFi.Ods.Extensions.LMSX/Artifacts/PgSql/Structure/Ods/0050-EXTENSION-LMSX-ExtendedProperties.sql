-- Extended Properties [lmsx].[Assignment] --
COMMENT ON TABLE lmsx.Assignment IS 'Course work assigned to students enrolled in a section.';
COMMENT ON COLUMN lmsx.Assignment.AssignmentIdentifier IS 'A unique string assigned to the assignment, based on the source system of record.';
COMMENT ON COLUMN lmsx.Assignment.SchoolId IS 'The identifier assigned to a school.';
COMMENT ON COLUMN lmsx.Assignment.LMSSourceSystemDescriptorId IS 'The system code or name providing the assignment data.';
COMMENT ON COLUMN lmsx.Assignment.Title IS 'The assignment title or name.';
COMMENT ON COLUMN lmsx.Assignment.AssignmentCategoryDescriptorId IS 'The category or type of assignment.';
COMMENT ON COLUMN lmsx.Assignment.AssignmentDescription IS 'The assignment description.';
COMMENT ON COLUMN lmsx.Assignment.StartDateTime IS 'The start date and time for the assignment. Students will have access to the assignment after this date.';
COMMENT ON COLUMN lmsx.Assignment.EndDateTime IS 'The end date and time for the assignment. Students will no longer have access to the assignment after this date.';
COMMENT ON COLUMN lmsx.Assignment.DueDateTime IS 'The date and time the assignment is due.';
COMMENT ON COLUMN lmsx.Assignment.MaxPoints IS 'The maximum number of points a student may receive for a submission of the assignment.';
COMMENT ON COLUMN lmsx.Assignment.SectionIdentifier IS 'The local identifier assigned to a section.';
COMMENT ON COLUMN lmsx.Assignment.LocalCourseCode IS 'The local code assigned by the School that identifies the course offering provided for the instruction of students.';
COMMENT ON COLUMN lmsx.Assignment.SessionName IS 'The identifier for the calendar for the academic session (e.g., 2010/11, 2011 Summer).';
COMMENT ON COLUMN lmsx.Assignment.SchoolYear IS 'The identifier for the school year.';

-- Extended Properties [lmsx].[AssignmentCategoryDescriptor] --
COMMENT ON TABLE lmsx.AssignmentCategoryDescriptor IS 'The category or type of assignment.';
COMMENT ON COLUMN lmsx.AssignmentCategoryDescriptor.AssignmentCategoryDescriptorId IS 'A unique identifier used as Primary Key, not derived from business logic, when acting as Foreign Key, references the parent table.';

-- Extended Properties [lmsx].[AssignmentSubmission] --
COMMENT ON TABLE lmsx.AssignmentSubmission IS 'A user''s submission of course work for an assignment.';
COMMENT ON COLUMN lmsx.AssignmentSubmission.AssignmentSubmissionIdentifier IS 'A unique numeric identifier assigned to the submission.';
COMMENT ON COLUMN lmsx.AssignmentSubmission.StudentUSI IS 'A unique alphanumeric code assigned to a student.';
COMMENT ON COLUMN lmsx.AssignmentSubmission.AssignmentIdentifier IS 'A unique string assigned to the assignment, based on the source system of record.';
COMMENT ON COLUMN lmsx.AssignmentSubmission.SchoolId IS 'The identifier assigned to a school.';
COMMENT ON COLUMN lmsx.AssignmentSubmission.SubmissionStatusDescriptorId IS 'The status of the submission in relation to the late acceptance policy.';
COMMENT ON COLUMN lmsx.AssignmentSubmission.SubmissionDateTime IS 'The date and time of the assignment submission.';
COMMENT ON COLUMN lmsx.AssignmentSubmission.EarnedPoints IS 'The points earned for the submission.';
COMMENT ON COLUMN lmsx.AssignmentSubmission.Grade IS 'The grade received for the submission.';

-- Extended Properties [lmsx].[AssignmentSubmissionType] --
COMMENT ON TABLE lmsx.AssignmentSubmissionType IS 'The type(s) of submissions available for the assignment.';
COMMENT ON COLUMN lmsx.AssignmentSubmissionType.AssignmentIdentifier IS 'A unique string assigned to the assignment, based on the source system of record.';
COMMENT ON COLUMN lmsx.AssignmentSubmissionType.SchoolId IS 'The identifier assigned to a school.';
COMMENT ON COLUMN lmsx.AssignmentSubmissionType.SubmissionTypeDescriptorId IS 'The type(s) of submissions available for the assignment.';

-- Extended Properties [lmsx].[LMSSourceSystemDescriptor] --
COMMENT ON TABLE lmsx.LMSSourceSystemDescriptor IS 'The Learning Management System (LMS) source system';
COMMENT ON COLUMN lmsx.LMSSourceSystemDescriptor.LMSSourceSystemDescriptorId IS 'A unique identifier used as Primary Key, not derived from business logic, when acting as Foreign Key, references the parent table.';

-- Extended Properties [lmsx].[SubmissionStatusDescriptor] --
COMMENT ON TABLE lmsx.SubmissionStatusDescriptor IS 'The status of the submission in relation to the late acceptance policy.';
COMMENT ON COLUMN lmsx.SubmissionStatusDescriptor.SubmissionStatusDescriptorId IS 'A unique identifier used as Primary Key, not derived from business logic, when acting as Foreign Key, references the parent table.';

-- Extended Properties [lmsx].[SubmissionTypeDescriptor] --
COMMENT ON TABLE lmsx.SubmissionTypeDescriptor IS 'The type(s) of submissions available for the assignment.';
COMMENT ON COLUMN lmsx.SubmissionTypeDescriptor.SubmissionTypeDescriptorId IS 'A unique identifier used as Primary Key, not derived from business logic, when acting as Foreign Key, references the parent table.';

