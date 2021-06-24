-- Table lmsx.Assignment --
CREATE TABLE lmsx.Assignment (
    AssignmentIdentifier VARCHAR(255) NOT NULL,
    SchoolId INT NOT NULL,
    LMSSourceSystemDescriptorId INT NOT NULL,
    Title VARCHAR(255) NOT NULL,
    AssignmentCategoryDescriptorId INT NOT NULL,
    AssignmentDescription VARCHAR(1024) NULL,
    StartDateTime TIMESTAMP NULL,
    EndDateTime TIMESTAMP NULL,
    DueDateTime TIMESTAMP NULL,
    MaxPoints INT NULL,
    SectionIdentifier VARCHAR(255) NOT NULL,
    LocalCourseCode VARCHAR(60) NOT NULL,
    SessionName VARCHAR(60) NOT NULL,
    SchoolYear SMALLINT NOT NULL,
    Discriminator VARCHAR(128) NULL,
    CreateDate TIMESTAMP NOT NULL,
    LastModifiedDate TIMESTAMP NOT NULL,
    Id UUID NOT NULL,
    CONSTRAINT Assignment_PK PRIMARY KEY (AssignmentIdentifier, SchoolId)
); 
ALTER TABLE lmsx.Assignment ALTER COLUMN CreateDate SET DEFAULT current_timestamp;
ALTER TABLE lmsx.Assignment ALTER COLUMN Id SET DEFAULT gen_random_uuid();
ALTER TABLE lmsx.Assignment ALTER COLUMN LastModifiedDate SET DEFAULT current_timestamp;

-- Table lmsx.AssignmentCategoryDescriptor --
CREATE TABLE lmsx.AssignmentCategoryDescriptor (
    AssignmentCategoryDescriptorId INT NOT NULL,
    CONSTRAINT AssignmentCategoryDescriptor_PK PRIMARY KEY (AssignmentCategoryDescriptorId)
); 

-- Table lmsx.AssignmentSubmission --
CREATE TABLE lmsx.AssignmentSubmission (
    AssignmentSubmissionIdentifier VARCHAR(255) NOT NULL,
    StudentUSI INT NOT NULL,
    AssignmentIdentifier VARCHAR(255) NOT NULL,
    SchoolId INT NOT NULL,
    SubmissionStatusDescriptorId INT NOT NULL,
    SubmissionDateTime TIMESTAMP NOT NULL,
    EarnedPoints INT NULL,
    Grade VARCHAR(20) NULL,
    Discriminator VARCHAR(128) NULL,
    CreateDate TIMESTAMP NOT NULL,
    LastModifiedDate TIMESTAMP NOT NULL,
    Id UUID NOT NULL,
    CONSTRAINT AssignmentSubmission_PK PRIMARY KEY (AssignmentSubmissionIdentifier, StudentUSI)
); 
ALTER TABLE lmsx.AssignmentSubmission ALTER COLUMN CreateDate SET DEFAULT current_timestamp;
ALTER TABLE lmsx.AssignmentSubmission ALTER COLUMN Id SET DEFAULT gen_random_uuid();
ALTER TABLE lmsx.AssignmentSubmission ALTER COLUMN LastModifiedDate SET DEFAULT current_timestamp;

-- Table lmsx.AssignmentSubmissionType --
CREATE TABLE lmsx.AssignmentSubmissionType (
    AssignmentIdentifier VARCHAR(255) NOT NULL,
    SchoolId INT NOT NULL,
    SubmissionTypeDescriptorId INT NOT NULL,
    CreateDate TIMESTAMP NOT NULL,
    CONSTRAINT AssignmentSubmissionType_PK PRIMARY KEY (AssignmentIdentifier, SchoolId, SubmissionTypeDescriptorId)
); 
ALTER TABLE lmsx.AssignmentSubmissionType ALTER COLUMN CreateDate SET DEFAULT current_timestamp;

-- Table lmsx.LMSSourceSystemDescriptor --
CREATE TABLE lmsx.LMSSourceSystemDescriptor (
    LMSSourceSystemDescriptorId INT NOT NULL,
    CONSTRAINT LMSSourceSystemDescriptor_PK PRIMARY KEY (LMSSourceSystemDescriptorId)
); 

-- Table lmsx.SubmissionStatusDescriptor --
CREATE TABLE lmsx.SubmissionStatusDescriptor (
    SubmissionStatusDescriptorId INT NOT NULL,
    CONSTRAINT SubmissionStatusDescriptor_PK PRIMARY KEY (SubmissionStatusDescriptorId)
); 

-- Table lmsx.SubmissionTypeDescriptor --
CREATE TABLE lmsx.SubmissionTypeDescriptor (
    SubmissionTypeDescriptorId INT NOT NULL,
    CONSTRAINT SubmissionTypeDescriptor_PK PRIMARY KEY (SubmissionTypeDescriptorId)
); 

