-- Table [fizz].[Assignment] --
CREATE TABLE [fizz].[Assignment] (
    [AssignmentIdentifier] [INT] IDENTITY,
    [SourceSystemIdentifier] [NVARCHAR](255) NOT NULL,
    [SourceSystem] [NVARCHAR](255) NOT NULL,
    [LMSSectionIdentifier] [INT] NOT NULL,
    [Title] [NVARCHAR](255) NOT NULL,
    [AssignmentCategory] [NVARCHAR](60) NOT NULL,
    [AssignmentDescription] [NVARCHAR](1024) NULL,
    [StartDateTime] [DATETIME2](7) NULL,
    [EndDateTime] [DATETIME2](7) NULL,
    [DueDateTime] [DATETIME2](7) NULL,
    [MaxPoints] [INT] NULL,
    [EntityStatus] [NVARCHAR](60) NOT NULL,
    [DeletedAt] [DATETIME2](7) NULL,
    [Discriminator] [NVARCHAR](128) NULL,
    [CreateDate] [DATETIME2] NOT NULL,
    [LastModifiedDate] [DATETIME2] NOT NULL,
    [Id] [UNIQUEIDENTIFIER] NOT NULL,
    CONSTRAINT [Assignment_PK] PRIMARY KEY CLUSTERED (
        [AssignmentIdentifier] ASC
    ) WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]
GO
ALTER TABLE [fizz].[Assignment] ADD CONSTRAINT [Assignment_DF_CreateDate] DEFAULT (getdate()) FOR [CreateDate]
GO
ALTER TABLE [fizz].[Assignment] ADD CONSTRAINT [Assignment_DF_Id] DEFAULT (newid()) FOR [Id]
GO
ALTER TABLE [fizz].[Assignment] ADD CONSTRAINT [Assignment_DF_LastModifiedDate] DEFAULT (getdate()) FOR [LastModifiedDate]
GO

-- Table [fizz].[AssignmentSubmission] --
CREATE TABLE [fizz].[AssignmentSubmission] (
    [LMSGradeIdentifier] [INT] IDENTITY,
    [SourceSystemIdentifier] [NVARCHAR](255) NOT NULL,
    [SourceSystem] [NVARCHAR](255) NOT NULL,
    [LMSUserIdentifier] [INT] NOT NULL,
    [AssignmentIdentifier] [INT] NOT NULL,
    [Status] [NVARCHAR](60) NOT NULL,
    [SubmissionDateTime] [DATETIME2](7) NOT NULL,
    [EarnedPoints] [INT] NULL,
    [Grade] [NVARCHAR](20) NULL,
    [EntityStatus] [NVARCHAR](60) NOT NULL,
    [DeletedAt] [DATETIME2](7) NULL,
    [Discriminator] [NVARCHAR](128) NULL,
    [CreateDate] [DATETIME2] NOT NULL,
    [LastModifiedDate] [DATETIME2] NOT NULL,
    [Id] [UNIQUEIDENTIFIER] NOT NULL,
    CONSTRAINT [AssignmentSubmission_PK] PRIMARY KEY CLUSTERED (
        [LMSGradeIdentifier] ASC
    ) WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]
GO
ALTER TABLE [fizz].[AssignmentSubmission] ADD CONSTRAINT [AssignmentSubmission_DF_CreateDate] DEFAULT (getdate()) FOR [CreateDate]
GO
ALTER TABLE [fizz].[AssignmentSubmission] ADD CONSTRAINT [AssignmentSubmission_DF_Id] DEFAULT (newid()) FOR [Id]
GO
ALTER TABLE [fizz].[AssignmentSubmission] ADD CONSTRAINT [AssignmentSubmission_DF_LastModifiedDate] DEFAULT (getdate()) FOR [LastModifiedDate]
GO

-- Table [fizz].[AssignmentSubmissionType] --
CREATE TABLE [fizz].[AssignmentSubmissionType] (
    [AssignmentIdentifier] [INT] NOT NULL,
    [SubmissionType] [NVARCHAR](60) NOT NULL,
    [CreateDate] [DATETIME2] NOT NULL,
    CONSTRAINT [AssignmentSubmissionType_PK] PRIMARY KEY CLUSTERED (
        [AssignmentIdentifier] ASC,
        [SubmissionType] ASC
    ) WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]
GO
ALTER TABLE [fizz].[AssignmentSubmissionType] ADD CONSTRAINT [AssignmentSubmissionType_DF_CreateDate] DEFAULT (getdate()) FOR [CreateDate]
GO

-- Table [fizz].[LMSGrade] --
CREATE TABLE [fizz].[LMSGrade] (
    [LMSGradeIdentifier] [INT] IDENTITY,
    [SourceSystemIdentifier] [NVARCHAR](255) NOT NULL,
    [SourceSystem] [NVARCHAR](255) NOT NULL,
    [LMSUserIdentifier] [INT] NOT NULL,
    [LMSSectionIdentifier] [INT] NOT NULL,
    [LMSUserLMSSectionAssociationIdentifier] [INT] NOT NULL,
    [Grade] [NVARCHAR](20) NOT NULL,
    [GradeType] [NVARCHAR](60) NULL,
    [EntityStatus] [NVARCHAR](60) NOT NULL,
    [DeletedAt] [DATETIME2](7) NULL,
    [Discriminator] [NVARCHAR](128) NULL,
    [CreateDate] [DATETIME2] NOT NULL,
    [LastModifiedDate] [DATETIME2] NOT NULL,
    [Id] [UNIQUEIDENTIFIER] NOT NULL,
    CONSTRAINT [LMSGrade_PK] PRIMARY KEY CLUSTERED (
        [LMSGradeIdentifier] ASC
    ) WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]
GO
ALTER TABLE [fizz].[LMSGrade] ADD CONSTRAINT [LMSGrade_DF_CreateDate] DEFAULT (getdate()) FOR [CreateDate]
GO
ALTER TABLE [fizz].[LMSGrade] ADD CONSTRAINT [LMSGrade_DF_Id] DEFAULT (newid()) FOR [Id]
GO
ALTER TABLE [fizz].[LMSGrade] ADD CONSTRAINT [LMSGrade_DF_LastModifiedDate] DEFAULT (getdate()) FOR [LastModifiedDate]
GO

-- Table [fizz].[LMSSection] --
CREATE TABLE [fizz].[LMSSection] (
    [LMSSectionIdentifier] [INT] IDENTITY,
    [SourceSystemIdentifier] [NVARCHAR](255) NOT NULL,
    [SourceSystem] [NVARCHAR](255) NOT NULL,
    [SISSectionIdentifier] [NVARCHAR](255) NULL,
    [Title] [NVARCHAR](255) NOT NULL,
    [SectionDescription] [NVARCHAR](1024) NULL,
    [Term] [NVARCHAR](60) NULL,
    [LMSSectionStatus] [NVARCHAR](60) NULL,
    [EntityStatus] [NVARCHAR](60) NOT NULL,
    [DeletedAt] [DATETIME2](7) NULL,
    [Discriminator] [NVARCHAR](128) NULL,
    [CreateDate] [DATETIME2] NOT NULL,
    [LastModifiedDate] [DATETIME2] NOT NULL,
    [Id] [UNIQUEIDENTIFIER] NOT NULL,
    CONSTRAINT [LMSSection_PK] PRIMARY KEY CLUSTERED (
        [LMSSectionIdentifier] ASC
    ) WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]
GO
ALTER TABLE [fizz].[LMSSection] ADD CONSTRAINT [LMSSection_DF_CreateDate] DEFAULT (getdate()) FOR [CreateDate]
GO
ALTER TABLE [fizz].[LMSSection] ADD CONSTRAINT [LMSSection_DF_Id] DEFAULT (newid()) FOR [Id]
GO
ALTER TABLE [fizz].[LMSSection] ADD CONSTRAINT [LMSSection_DF_LastModifiedDate] DEFAULT (getdate()) FOR [LastModifiedDate]
GO

-- Table [fizz].[LMSUser] --
CREATE TABLE [fizz].[LMSUser] (
    [LMSUserIdentifier] [INT] IDENTITY,
    [SourceSystemIdentifier] [NVARCHAR](255) NOT NULL,
    [SourceSystem] [NVARCHAR](255) NOT NULL,
    [UserRole] [NVARCHAR](60) NOT NULL,
    [SISUserIdentifier] [NVARCHAR](255) NULL,
    [LocalUserIdentifier] [NVARCHAR](255) NULL,
    [Name] [NVARCHAR](255) NOT NULL,
    [EmailAddress] [NVARCHAR](255) NOT NULL,
    [EntityStatus] [NVARCHAR](60) NOT NULL,
    [DeletedAt] [DATETIME2](7) NULL,
    [Discriminator] [NVARCHAR](128) NULL,
    [CreateDate] [DATETIME2] NOT NULL,
    [LastModifiedDate] [DATETIME2] NOT NULL,
    [Id] [UNIQUEIDENTIFIER] NOT NULL,
    CONSTRAINT [LMSUser_PK] PRIMARY KEY CLUSTERED (
        [LMSUserIdentifier] ASC
    ) WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]
GO
ALTER TABLE [fizz].[LMSUser] ADD CONSTRAINT [LMSUser_DF_CreateDate] DEFAULT (getdate()) FOR [CreateDate]
GO
ALTER TABLE [fizz].[LMSUser] ADD CONSTRAINT [LMSUser_DF_Id] DEFAULT (newid()) FOR [Id]
GO
ALTER TABLE [fizz].[LMSUser] ADD CONSTRAINT [LMSUser_DF_LastModifiedDate] DEFAULT (getdate()) FOR [LastModifiedDate]
GO

-- Table [fizz].[LMSUserActivity] --
CREATE TABLE [fizz].[LMSUserActivity] (
    [LMSUserActivityIdentifier] [INT] IDENTITY,
    [SourceSystemIdentifier] [NVARCHAR](255) NOT NULL,
    [SourceSystem] [NVARCHAR](255) NOT NULL,
    [LMSUserIdentifier] [INT] NOT NULL,
    [LMSSectionIdentifier] [INT] NULL,
    [AssignmentIdentifier] [INT] NULL,
    [ActivityType] [NVARCHAR](60) NOT NULL,
    [ActivityDateTime] [DATETIME2](7) NOT NULL,
    [ActivityStatus] [NVARCHAR](60) NOT NULL,
    [Content] [NVARCHAR](1024) NULL,
    [ActivityTimeInMinutes] [INT] NULL,
    [EntityStatus] [NVARCHAR](60) NOT NULL,
    [DeletedAt] [DATETIME2](7) NULL,
    [Discriminator] [NVARCHAR](128) NULL,
    [CreateDate] [DATETIME2] NOT NULL,
    [LastModifiedDate] [DATETIME2] NOT NULL,
    [Id] [UNIQUEIDENTIFIER] NOT NULL,
    CONSTRAINT [LMSUserActivity_PK] PRIMARY KEY CLUSTERED (
        [LMSUserActivityIdentifier] ASC
    ) WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]
GO
ALTER TABLE [fizz].[LMSUserActivity] ADD CONSTRAINT [LMSUserActivity_DF_CreateDate] DEFAULT (getdate()) FOR [CreateDate]
GO
ALTER TABLE [fizz].[LMSUserActivity] ADD CONSTRAINT [LMSUserActivity_DF_Id] DEFAULT (newid()) FOR [Id]
GO
ALTER TABLE [fizz].[LMSUserActivity] ADD CONSTRAINT [LMSUserActivity_DF_LastModifiedDate] DEFAULT (getdate()) FOR [LastModifiedDate]
GO

-- Table [fizz].[LMSUserAttendanceEvent] --
CREATE TABLE [fizz].[LMSUserAttendanceEvent] (
    [LMSUserAttendanceEventIdentifier] [INT] IDENTITY,
    [SourceSystemIdentifier] [NVARCHAR](255) NOT NULL,
    [SourceSystem] [NVARCHAR](255) NOT NULL,
    [LMSUserIdentifier] [INT] NOT NULL,
    [LMSSectionIdentifier] [INT] NULL,
    [LMSUserLMSSectionAssociationIdentifier] [INT] NULL,
    [EventDate] [DATE] NOT NULL,
    [Status] [NVARCHAR](60) NOT NULL,
    [EntityStatus] [NVARCHAR](60) NOT NULL,
    [DeletedAt] [DATETIME2](7) NULL,
    [Discriminator] [NVARCHAR](128) NULL,
    [CreateDate] [DATETIME2] NOT NULL,
    [LastModifiedDate] [DATETIME2] NOT NULL,
    [Id] [UNIQUEIDENTIFIER] NOT NULL,
    CONSTRAINT [LMSUserAttendanceEvent_PK] PRIMARY KEY CLUSTERED (
        [LMSUserAttendanceEventIdentifier] ASC
    ) WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]
GO
ALTER TABLE [fizz].[LMSUserAttendanceEvent] ADD CONSTRAINT [LMSUserAttendanceEvent_DF_CreateDate] DEFAULT (getdate()) FOR [CreateDate]
GO
ALTER TABLE [fizz].[LMSUserAttendanceEvent] ADD CONSTRAINT [LMSUserAttendanceEvent_DF_Id] DEFAULT (newid()) FOR [Id]
GO
ALTER TABLE [fizz].[LMSUserAttendanceEvent] ADD CONSTRAINT [LMSUserAttendanceEvent_DF_LastModifiedDate] DEFAULT (getdate()) FOR [LastModifiedDate]
GO

-- Table [fizz].[LMSUserLMSSectionAssociation] --
CREATE TABLE [fizz].[LMSUserLMSSectionAssociation] (
    [LMSSectionIdentifier] [INT] NOT NULL,
    [LMSUserIdentifier] [INT] NOT NULL,
    [LMSUserLMSSectionAssociationIdentifier] [INT] IDENTITY,
    [SourceSystemIdentifier] [NVARCHAR](255) NOT NULL,
    [SourceSystem] [NVARCHAR](255) NOT NULL,
    [EnrollmentStatus] [NVARCHAR](60) NOT NULL,
    [StartDate] [DATE] NOT NULL,
    [EndDate] [DATE] NOT NULL,
    [EntityStatus] [NVARCHAR](60) NOT NULL,
    [DeletedAt] [DATETIME2](7) NULL,
    [Discriminator] [NVARCHAR](128) NULL,
    [CreateDate] [DATETIME2] NOT NULL,
    [LastModifiedDate] [DATETIME2] NOT NULL,
    [Id] [UNIQUEIDENTIFIER] NOT NULL,
    CONSTRAINT [LMSUserLMSSectionAssociation_PK] PRIMARY KEY CLUSTERED (
        [LMSSectionIdentifier] ASC,
        [LMSUserIdentifier] ASC,
        [LMSUserLMSSectionAssociationIdentifier] ASC
    ) WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]
GO
ALTER TABLE [fizz].[LMSUserLMSSectionAssociation] ADD CONSTRAINT [LMSUserLMSSectionAssociation_DF_CreateDate] DEFAULT (getdate()) FOR [CreateDate]
GO
ALTER TABLE [fizz].[LMSUserLMSSectionAssociation] ADD CONSTRAINT [LMSUserLMSSectionAssociation_DF_Id] DEFAULT (newid()) FOR [Id]
GO
ALTER TABLE [fizz].[LMSUserLMSSectionAssociation] ADD CONSTRAINT [LMSUserLMSSectionAssociation_DF_LastModifiedDate] DEFAULT (getdate()) FOR [LastModifiedDate]
GO

