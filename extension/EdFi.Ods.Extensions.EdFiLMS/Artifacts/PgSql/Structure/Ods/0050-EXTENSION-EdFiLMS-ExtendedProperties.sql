-- Extended Properties [edfilms].[Assignment] --
COMMENT ON TABLE edfilms.Assignment IS 'Course work assigned to students enrolled in a section.';
COMMENT ON COLUMN edfilms.Assignment.AssignmentIdentifier IS 'A unique string assigned to the assignment, based on the source system of record.';
COMMENT ON COLUMN edfilms.Assignment.SourceSystemDescriptorId IS 'The system code or name providing the assignment data.';
COMMENT ON COLUMN edfilms.Assignment.Title IS 'The assignment title or name.';
COMMENT ON COLUMN edfilms.Assignment.AssignmentCategoryDescriptorId IS 'The category or type of assignment.';
COMMENT ON COLUMN edfilms.Assignment.AssignmentDescription IS 'The assignment description.';
COMMENT ON COLUMN edfilms.Assignment.StartDateTime IS 'The start date and time for the assignment. Students will have access to the assignment after this date.';
COMMENT ON COLUMN edfilms.Assignment.EndDateTime IS 'The end date and time for the assignment. Students will no longer have access to the assignment after this date.';
COMMENT ON COLUMN edfilms.Assignment.DueDateTime IS 'The date and time the assignment is due.';
COMMENT ON COLUMN edfilms.Assignment.MaxPoints IS 'The maximum number of points a student may receive for a submission of the assignment.';
COMMENT ON COLUMN edfilms.Assignment.SectionIdentifier IS 'The local identifier assigned to a section.';
COMMENT ON COLUMN edfilms.Assignment.LocalCourseCode IS 'The local code assigned by the School that identifies the course offering provided for the instruction of students.';
COMMENT ON COLUMN edfilms.Assignment.SessionName IS 'The identifier for the calendar for the academic session (e.g., 2010/11, 2011 Summer).';
COMMENT ON COLUMN edfilms.Assignment.SchoolYear IS 'The identifier for the school year.';
COMMENT ON COLUMN edfilms.Assignment.SchoolId IS 'The identifier assigned to a school.';

-- Extended Properties [edfilms].[AssignmentCategoryDescriptor] --
COMMENT ON TABLE edfilms.AssignmentCategoryDescriptor IS 'The category or type of assignment.';
COMMENT ON COLUMN edfilms.AssignmentCategoryDescriptor.AssignmentCategoryDescriptorId IS 'A unique identifier used as Primary Key, not derived from business logic, when acting as Foreign Key, references the parent table.';

-- Extended Properties [edfilms].[AssignmentSubmission] --
COMMENT ON TABLE edfilms.AssignmentSubmission IS 'A user''s submission of course work for an assignment.';
COMMENT ON COLUMN edfilms.AssignmentSubmission.AssignmentSubmissionIdentifier IS 'A unique numeric identifier assigned to the submission.';
COMMENT ON COLUMN edfilms.AssignmentSubmission.AssignmentIdentifier IS 'A unique string assigned to the assignment, based on the source system of record.';
COMMENT ON COLUMN edfilms.AssignmentSubmission.StudentUSI IS 'A unique alphanumeric code assigned to a student.';
COMMENT ON COLUMN edfilms.AssignmentSubmission.SubmissionStatusDescriptorId IS 'The status of the submission in relation to the late acceptance policy.';
COMMENT ON COLUMN edfilms.AssignmentSubmission.SubmissionDateTime IS 'The date and time of the assignment submission.';
COMMENT ON COLUMN edfilms.AssignmentSubmission.EarnedPoints IS 'The points earned for the submission.';
COMMENT ON COLUMN edfilms.AssignmentSubmission.Grade IS 'The grade received for the submission.';

-- Extended Properties [edfilms].[AssignmentSubmissionType] --
COMMENT ON TABLE edfilms.AssignmentSubmissionType IS 'The type(s) of submissions available for the assignment.';
COMMENT ON COLUMN edfilms.AssignmentSubmissionType.AssignmentIdentifier IS 'A unique string assigned to the assignment, based on the source system of record.';
COMMENT ON COLUMN edfilms.AssignmentSubmissionType.SubmissionTypeDescriptorId IS 'The type(s) of submissions available for the assignment.';

-- Extended Properties [edfilms].[SubmissionStatusDescriptor] --
COMMENT ON TABLE edfilms.SubmissionStatusDescriptor IS 'The status of the submission in relation to the late acceptance policy.';
COMMENT ON COLUMN edfilms.SubmissionStatusDescriptor.SubmissionStatusDescriptorId IS 'A unique identifier used as Primary Key, not derived from business logic, when acting as Foreign Key, references the parent table.';

-- Extended Properties [edfilms].[SubmissionTypeDescriptor] --
COMMENT ON TABLE edfilms.SubmissionTypeDescriptor IS 'The type(s) of submissions available for the assignment.';
COMMENT ON COLUMN edfilms.SubmissionTypeDescriptor.SubmissionTypeDescriptorId IS 'A unique identifier used as Primary Key, not derived from business logic, when acting as Foreign Key, references the parent table.';

