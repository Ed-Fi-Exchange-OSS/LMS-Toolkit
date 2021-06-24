-- Table [lmsx].[Assignment] --
CREATE TABLE [lmsx].[Assignment] (
    [AssignmentIdentifier] [NVARCHAR](255) NOT NULL,
    [SchoolId] [INT] NOT NULL,
    [LMSSourceSystemDescriptorId] [INT] NOT NULL,
    [Title] [NVARCHAR](255) NOT NULL,
    [AssignmentCategoryDescriptorId] [INT] NOT NULL,
    [AssignmentDescription] [NVARCHAR](1024) NULL,
    [StartDateTime] [DATETIME2](7) NULL,
    [EndDateTime] [DATETIME2](7) NULL,
    [DueDateTime] [DATETIME2](7) NULL,
    [MaxPoints] [INT] NULL,
    [SectionIdentifier] [NVARCHAR](255) NOT NULL,
    [LocalCourseCode] [NVARCHAR](60) NOT NULL,
    [SessionName] [NVARCHAR](60) NOT NULL,
    [SchoolYear] [SMALLINT] NOT NULL,
    [Discriminator] [NVARCHAR](128) NULL,
    [CreateDate] [DATETIME2] NOT NULL,
    [LastModifiedDate] [DATETIME2] NOT NULL,
    [Id] [UNIQUEIDENTIFIER] NOT NULL,
    CONSTRAINT [Assignment_PK] PRIMARY KEY CLUSTERED (
        [AssignmentIdentifier] ASC,
        [SchoolId] ASC
    ) WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]
GO
ALTER TABLE [lmsx].[Assignment] ADD CONSTRAINT [Assignment_DF_CreateDate] DEFAULT (getdate()) FOR [CreateDate]
GO
ALTER TABLE [lmsx].[Assignment] ADD CONSTRAINT [Assignment_DF_Id] DEFAULT (newid()) FOR [Id]
GO
ALTER TABLE [lmsx].[Assignment] ADD CONSTRAINT [Assignment_DF_LastModifiedDate] DEFAULT (getdate()) FOR [LastModifiedDate]
GO

-- Table [lmsx].[AssignmentCategoryDescriptor] --
CREATE TABLE [lmsx].[AssignmentCategoryDescriptor] (
    [AssignmentCategoryDescriptorId] [INT] NOT NULL,
    CONSTRAINT [AssignmentCategoryDescriptor_PK] PRIMARY KEY CLUSTERED (
        [AssignmentCategoryDescriptorId] ASC
    ) WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]
GO

-- Table [lmsx].[AssignmentSubmission] --
CREATE TABLE [lmsx].[AssignmentSubmission] (
    [AssignmentSubmissionIdentifier] [NVARCHAR](255) NOT NULL,
    [StudentUSI] [INT] NOT NULL,
    [AssignmentIdentifier] [NVARCHAR](255) NOT NULL,
    [SchoolId] [INT] NOT NULL,
    [SubmissionStatusDescriptorId] [INT] NOT NULL,
    [SubmissionDateTime] [DATETIME2](7) NOT NULL,
    [EarnedPoints] [INT] NULL,
    [Grade] [NVARCHAR](20) NULL,
    [Discriminator] [NVARCHAR](128) NULL,
    [CreateDate] [DATETIME2] NOT NULL,
    [LastModifiedDate] [DATETIME2] NOT NULL,
    [Id] [UNIQUEIDENTIFIER] NOT NULL,
    CONSTRAINT [AssignmentSubmission_PK] PRIMARY KEY CLUSTERED (
        [AssignmentSubmissionIdentifier] ASC,
        [StudentUSI] ASC
    ) WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]
GO
ALTER TABLE [lmsx].[AssignmentSubmission] ADD CONSTRAINT [AssignmentSubmission_DF_CreateDate] DEFAULT (getdate()) FOR [CreateDate]
GO
ALTER TABLE [lmsx].[AssignmentSubmission] ADD CONSTRAINT [AssignmentSubmission_DF_Id] DEFAULT (newid()) FOR [Id]
GO
ALTER TABLE [lmsx].[AssignmentSubmission] ADD CONSTRAINT [AssignmentSubmission_DF_LastModifiedDate] DEFAULT (getdate()) FOR [LastModifiedDate]
GO

-- Table [lmsx].[AssignmentSubmissionType] --
CREATE TABLE [lmsx].[AssignmentSubmissionType] (
    [AssignmentIdentifier] [NVARCHAR](255) NOT NULL,
    [SchoolId] [INT] NOT NULL,
    [SubmissionTypeDescriptorId] [INT] NOT NULL,
    [CreateDate] [DATETIME2] NOT NULL,
    CONSTRAINT [AssignmentSubmissionType_PK] PRIMARY KEY CLUSTERED (
        [AssignmentIdentifier] ASC,
        [SchoolId] ASC,
        [SubmissionTypeDescriptorId] ASC
    ) WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]
GO
ALTER TABLE [lmsx].[AssignmentSubmissionType] ADD CONSTRAINT [AssignmentSubmissionType_DF_CreateDate] DEFAULT (getdate()) FOR [CreateDate]
GO

-- Table [lmsx].[LMSSourceSystemDescriptor] --
CREATE TABLE [lmsx].[LMSSourceSystemDescriptor] (
    [LMSSourceSystemDescriptorId] [INT] NOT NULL,
    CONSTRAINT [LMSSourceSystemDescriptor_PK] PRIMARY KEY CLUSTERED (
        [LMSSourceSystemDescriptorId] ASC
    ) WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]
GO

-- Table [lmsx].[SubmissionStatusDescriptor] --
CREATE TABLE [lmsx].[SubmissionStatusDescriptor] (
    [SubmissionStatusDescriptorId] [INT] NOT NULL,
    CONSTRAINT [SubmissionStatusDescriptor_PK] PRIMARY KEY CLUSTERED (
        [SubmissionStatusDescriptorId] ASC
    ) WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]
GO

-- Table [lmsx].[SubmissionTypeDescriptor] --
CREATE TABLE [lmsx].[SubmissionTypeDescriptor] (
    [SubmissionTypeDescriptorId] [INT] NOT NULL,
    CONSTRAINT [SubmissionTypeDescriptor_PK] PRIMARY KEY CLUSTERED (
        [SubmissionTypeDescriptorId] ASC
    ) WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]
GO

