-- Table edfilms.Assignment --
CREATE TABLE edfilms.Assignment (
    AssignmentIdentifier VARCHAR(255) NOT NULL,
    LMSSourceSystemDescriptorId INT NOT NULL,
    Title VARCHAR(255) NOT NULL,
    AssignmentCategoryDescriptorId INT NOT NULL,
    AssignmentDescription VARCHAR(1024) NULL,
    StartDateTime TIMESTAMP NULL,
    EndDateTime TIMESTAMP NULL,
    DueDateTime TIMESTAMP NULL,
    MaxPoints INT NULL,
    SectionIdentifier VARCHAR(255) NOT NULL,
    LocalCourseCode VARCHAR(60) NULL,
    SessionName VARCHAR(60) NULL,
    SchoolYear SMALLINT NULL,
    SchoolId INT NULL,
    Discriminator VARCHAR(128) NULL,
    CreateDate TIMESTAMP NOT NULL,
    LastModifiedDate TIMESTAMP NOT NULL,
    Id UUID NOT NULL,
    CONSTRAINT Assignment_PK PRIMARY KEY (AssignmentIdentifier)
); 
ALTER TABLE edfilms.Assignment ALTER COLUMN CreateDate SET DEFAULT current_timestamp;
ALTER TABLE edfilms.Assignment ALTER COLUMN Id SET DEFAULT gen_random_uuid();
ALTER TABLE edfilms.Assignment ALTER COLUMN LastModifiedDate SET DEFAULT current_timestamp;

-- Table edfilms.AssignmentCategoryDescriptor --
CREATE TABLE edfilms.AssignmentCategoryDescriptor (
    AssignmentCategoryDescriptorId INT NOT NULL,
    CONSTRAINT AssignmentCategoryDescriptor_PK PRIMARY KEY (AssignmentCategoryDescriptorId)
); 

-- Table edfilms.AssignmentSubmission --
CREATE TABLE edfilms.AssignmentSubmission (
    AssignmentSubmissionIdentifier VARCHAR(255) NOT NULL,
    AssignmentIdentifier VARCHAR(255) NOT NULL,
    StudentUSI INT NOT NULL,
    SubmissionStatusDescriptorId INT NOT NULL,
    SubmissionDateTime TIMESTAMP NOT NULL,
    EarnedPoints INT NULL,
    Grade VARCHAR(20) NULL,
    Discriminator VARCHAR(128) NULL,
    CreateDate TIMESTAMP NOT NULL,
    LastModifiedDate TIMESTAMP NOT NULL,
    Id UUID NOT NULL,
    CONSTRAINT AssignmentSubmission_PK PRIMARY KEY (AssignmentSubmissionIdentifier)
); 
ALTER TABLE edfilms.AssignmentSubmission ALTER COLUMN CreateDate SET DEFAULT current_timestamp;
ALTER TABLE edfilms.AssignmentSubmission ALTER COLUMN Id SET DEFAULT gen_random_uuid();
ALTER TABLE edfilms.AssignmentSubmission ALTER COLUMN LastModifiedDate SET DEFAULT current_timestamp;

-- Table edfilms.AssignmentSubmissionType --
CREATE TABLE edfilms.AssignmentSubmissionType (
    AssignmentIdentifier VARCHAR(255) NOT NULL,
    SubmissionTypeDescriptorId INT NOT NULL,
    CreateDate TIMESTAMP NOT NULL,
    CONSTRAINT AssignmentSubmissionType_PK PRIMARY KEY (AssignmentIdentifier, SubmissionTypeDescriptorId)
); 
ALTER TABLE edfilms.AssignmentSubmissionType ALTER COLUMN CreateDate SET DEFAULT current_timestamp;

-- Table edfilms.LMSSourceSystemDescriptor --
CREATE TABLE edfilms.LMSSourceSystemDescriptor (
    LMSSourceSystemDescriptorId INT NOT NULL,
    CONSTRAINT LMSSourceSystemDescriptor_PK PRIMARY KEY (LMSSourceSystemDescriptorId)
); 

-- Table edfilms.SubmissionStatusDescriptor --
CREATE TABLE edfilms.SubmissionStatusDescriptor (
    SubmissionStatusDescriptorId INT NOT NULL,
    CONSTRAINT SubmissionStatusDescriptor_PK PRIMARY KEY (SubmissionStatusDescriptorId)
); 

-- Table edfilms.SubmissionTypeDescriptor --
CREATE TABLE edfilms.SubmissionTypeDescriptor (
    SubmissionTypeDescriptorId INT NOT NULL,
    CONSTRAINT SubmissionTypeDescriptor_PK PRIMARY KEY (SubmissionTypeDescriptorId)
); 

