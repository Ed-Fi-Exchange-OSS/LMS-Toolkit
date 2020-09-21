CREATE TABLE lms.[User] (
    Id INT NOT NULL IDENTITY,
    SourceSystemIdentifier VARCHAR(50) NOT NULL,
    SourceSystem VARCHAR(50) NOT NULL,
    UserRole VARCHAR(50) NOT NULL,
    LocalUserId VARCHAR(50),
    SISUserIdentifier VARCHAR(50),
    [Name] VARCHAR(250),
    EmailAddress VARCHAR(320),
    EntityStatus VARCHAR(50),
    CreateDate DATETIME2 NOT NULL CONSTRAINT DF_User_CreateDate DEFAULT (getdate()),
    LastModifiedDate DATETIME2 NOT NULL CONSTRAINT DF_User_LastModifiedDate DEFAULT (getdate()),
    CONSTRAINT PK_User PRIMARY KEY CLUSTERED (
        Id ASC
    ) WITH(
        PAD_INDEX = OFF,
        STATISTICS_NORECOMPUTE = OFF,
        IGNORE_DUP_KEY = OFF,
        ALLOW_ROW_LOCKS = ON,
        ALLOW_PAGE_LOCKS = ON
    ) ON [PRIMARY],
    CONSTRAINT UK_SourceSystem UNIQUE (
        SourceSystemIdentifier,
        SourceSystem
    )
) ON [PRIMARY];
