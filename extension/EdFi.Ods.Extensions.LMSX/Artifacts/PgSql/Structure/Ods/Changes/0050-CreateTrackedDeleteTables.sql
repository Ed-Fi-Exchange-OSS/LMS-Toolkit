CREATE TABLE tracked_deletes_edfilms.Assignment
(
       AssignmentIdentifier VARCHAR(255) NOT NULL,
       Id UUID NOT NULL,
       ChangeVersion BIGINT NOT NULL,
       CONSTRAINT Assignment_PK PRIMARY KEY (ChangeVersion)
);

CREATE TABLE tracked_deletes_edfilms.AssignmentCategoryDescriptor
(
       AssignmentCategoryDescriptorId INT NOT NULL,
       Id UUID NOT NULL,
       ChangeVersion BIGINT NOT NULL,
       CONSTRAINT AssignmentCategoryDescriptor_PK PRIMARY KEY (ChangeVersion)
);

CREATE TABLE tracked_deletes_edfilms.AssignmentSubmission
(
       AssignmentSubmissionIdentifier VARCHAR(255) NOT NULL,
       Id UUID NOT NULL,
       ChangeVersion BIGINT NOT NULL,
       CONSTRAINT AssignmentSubmission_PK PRIMARY KEY (ChangeVersion)
);

CREATE TABLE tracked_deletes_edfilms.LMSSourceSystemDescriptor
(
       LMSSourceSystemDescriptorId INT NOT NULL,
       Id UUID NOT NULL,
       ChangeVersion BIGINT NOT NULL,
       CONSTRAINT LMSSourceSystemDescriptor_PK PRIMARY KEY (ChangeVersion)
);

CREATE TABLE tracked_deletes_edfilms.SubmissionStatusDescriptor
(
       SubmissionStatusDescriptorId INT NOT NULL,
       Id UUID NOT NULL,
       ChangeVersion BIGINT NOT NULL,
       CONSTRAINT SubmissionStatusDescriptor_PK PRIMARY KEY (ChangeVersion)
);

CREATE TABLE tracked_deletes_edfilms.SubmissionTypeDescriptor
(
       SubmissionTypeDescriptorId INT NOT NULL,
       Id UUID NOT NULL,
       ChangeVersion BIGINT NOT NULL,
       CONSTRAINT SubmissionTypeDescriptor_PK PRIMARY KEY (ChangeVersion)
);

