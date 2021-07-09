CREATE TABLE [tracked_deletes_lmsx].[Assignment]
(
       AssignmentIdentifier [NVARCHAR](255) NOT NULL,
       Namespace [NVARCHAR](255) NOT NULL,
       Id uniqueidentifier NOT NULL,
       ChangeVersion bigint NOT NULL,
       CONSTRAINT PK_Assignment PRIMARY KEY CLUSTERED (ChangeVersion)
)
CREATE TABLE [tracked_deletes_lmsx].[AssignmentCategoryDescriptor]
(
       AssignmentCategoryDescriptorId [INT] NOT NULL,
       Id uniqueidentifier NOT NULL,
       ChangeVersion bigint NOT NULL,
       CONSTRAINT PK_AssignmentCategoryDescriptor PRIMARY KEY CLUSTERED (ChangeVersion)
)
CREATE TABLE [tracked_deletes_lmsx].[AssignmentSubmission]
(
       AssignmentSubmissionIdentifier [NVARCHAR](255) NOT NULL,
       Namespace [NVARCHAR](255) NOT NULL,
       StudentUSI [INT] NOT NULL,
       Id uniqueidentifier NOT NULL,
       ChangeVersion bigint NOT NULL,
       CONSTRAINT PK_AssignmentSubmission PRIMARY KEY CLUSTERED (ChangeVersion)
)
CREATE TABLE [tracked_deletes_lmsx].[LMSSourceSystemDescriptor]
(
       LMSSourceSystemDescriptorId [INT] NOT NULL,
       Id uniqueidentifier NOT NULL,
       ChangeVersion bigint NOT NULL,
       CONSTRAINT PK_LMSSourceSystemDescriptor PRIMARY KEY CLUSTERED (ChangeVersion)
)
CREATE TABLE [tracked_deletes_lmsx].[SubmissionStatusDescriptor]
(
       SubmissionStatusDescriptorId [INT] NOT NULL,
       Id uniqueidentifier NOT NULL,
       ChangeVersion bigint NOT NULL,
       CONSTRAINT PK_SubmissionStatusDescriptor PRIMARY KEY CLUSTERED (ChangeVersion)
)
CREATE TABLE [tracked_deletes_lmsx].[SubmissionTypeDescriptor]
(
       SubmissionTypeDescriptorId [INT] NOT NULL,
       Id uniqueidentifier NOT NULL,
       ChangeVersion bigint NOT NULL,
       CONSTRAINT PK_SubmissionTypeDescriptor PRIMARY KEY CLUSTERED (ChangeVersion)
)
