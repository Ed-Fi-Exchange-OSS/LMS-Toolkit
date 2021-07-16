CREATE TABLE tracked_deletes_lmsx.Assignment
(
       AssignmentIdentifier VARCHAR(255) NOT NULL,
       Namespace VARCHAR(255) NOT NULL,
       Id UUID NOT NULL,
       ChangeVersion BIGINT NOT NULL,
       CONSTRAINT Assignment_PK PRIMARY KEY (ChangeVersion)
);

CREATE TABLE tracked_deletes_lmsx.AssignmentCategoryDescriptor
(
       AssignmentCategoryDescriptorId INT NOT NULL,
       Id UUID NOT NULL,
       ChangeVersion BIGINT NOT NULL,
       CONSTRAINT AssignmentCategoryDescriptor_PK PRIMARY KEY (ChangeVersion)
);

CREATE TABLE tracked_deletes_lmsx.AssignmentSubmission
(
       AssignmentSubmissionIdentifier VARCHAR(255) NOT NULL,
       Namespace VARCHAR(255) NOT NULL,
       StudentUSI INT NOT NULL,
       Id UUID NOT NULL,
       ChangeVersion BIGINT NOT NULL,
       CONSTRAINT AssignmentSubmission_PK PRIMARY KEY (ChangeVersion)
);

CREATE TABLE tracked_deletes_lmsx.LMSSourceSystemDescriptor
(
       LMSSourceSystemDescriptorId INT NOT NULL,
       Id UUID NOT NULL,
       ChangeVersion BIGINT NOT NULL,
       CONSTRAINT LMSSourceSystemDescriptor_PK PRIMARY KEY (ChangeVersion)
);

CREATE TABLE tracked_deletes_lmsx.SubmissionStatusDescriptor
(
       SubmissionStatusDescriptorId INT NOT NULL,
       Id UUID NOT NULL,
       ChangeVersion BIGINT NOT NULL,
       CONSTRAINT SubmissionStatusDescriptor_PK PRIMARY KEY (ChangeVersion)
);

CREATE TABLE tracked_deletes_lmsx.SubmissionTypeDescriptor
(
       SubmissionTypeDescriptorId INT NOT NULL,
       Id UUID NOT NULL,
       ChangeVersion BIGINT NOT NULL,
       CONSTRAINT SubmissionTypeDescriptor_PK PRIMARY KEY (ChangeVersion)
);

