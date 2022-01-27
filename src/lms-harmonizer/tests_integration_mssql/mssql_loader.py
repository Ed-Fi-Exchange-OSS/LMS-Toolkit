# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.
# from os import path

from pyodbc import Connection, Cursor


SCHOOL_ID = 149
SCHOOL_YEAR = 153
SESSION_NAME = "session name test"
COURSE_CODE = "Local course code test"
USER_ROLE = "student"
GRADE = "A-"


def insert_lms_user(
    connection: Connection, sis_identifier: str, email_address: str, source_system: str
):
    connection.execute(
        f"""
    INSERT INTO [lms].[LMSUser]
           ([SourceSystemIdentifier]
           ,[SourceSystem]
           ,[UserRole]
           ,[SISUserIdentifier]
           ,[LocalUserIdentifier]
           ,[Name]
           ,[EmailAddress]
           ,[SourceCreateDate]
           ,[SourceLastModifiedDate]
           ,[CreateDate]
           ,[LastModifiedDate]
           ,[DeletedAt])
     VALUES
           (N'{sis_identifier}'
           ,N'{source_system}'
           ,N'{USER_ROLE}'
           ,N'{sis_identifier}1'
           ,N'{sis_identifier}2'
           ,N'{sis_identifier}3'
           ,N'{email_address}'
           ,NULL
           ,NULL
           ,CAST(N'2021-01-01 00:00:00' AS DateTime)
           ,CAST(N'2021-01-01 00:00:00' AS DateTime)
           ,NULL
           )
"""
    )


def insert_lms_user_deleted(
    connection: Connection, sis_identifier: str, email_address: str, source_system: str
):
    connection.execute(
        f"""
    INSERT INTO [lms].[LMSUser]
           ([SourceSystemIdentifier]
           ,[SourceSystem]
           ,[UserRole]
           ,[SISUserIdentifier]
           ,[LocalUserIdentifier]
           ,[Name]
           ,[EmailAddress]
           ,[SourceCreateDate]
           ,[SourceLastModifiedDate]
           ,[CreateDate]
           ,[LastModifiedDate]
           ,[DeletedAt])
     VALUES
           (N'{sis_identifier}'
           ,N'{source_system}'
           ,N'{USER_ROLE}'
           ,N'{sis_identifier}1'
           ,N'{sis_identifier}2'
           ,N'{sis_identifier}3'
           ,N'{email_address}'
           ,NULL
           ,NULL
           ,CAST(N'2021-01-01 00:00:00' AS DateTime)
           ,CAST(N'2021-01-01 00:00:00' AS DateTime)
           ,CAST(N'2021-01-02 00:00:00' AS DateTime)
           )
"""
    )


def insert_edfi_student(
    connection: Connection,
    student_unique_id: str,
    id: str = "00000000-0000-0000-0000-000000000000",
):
    connection.execute(
        f"""
INSERT INTO [edfi].[Student]
           ([PersonalTitlePrefix]
           ,[FirstName]
           ,[MiddleName]
           ,[LastSurname]
           ,[GenerationCodeSuffix]
           ,[MaidenName]
           ,[BirthDate]
           ,[BirthCity]
           ,[BirthStateAbbreviationDescriptorId]
           ,[BirthInternationalProvince]
           ,[BirthCountryDescriptorId]
           ,[DateEnteredUS]
           ,[MultipleBirthStatus]
           ,[BirthSexDescriptorId]
           ,[CitizenshipStatusDescriptorId]
           ,[StudentUniqueId]
           ,[CreateDate]
           ,[LastModifiedDate]
           ,[Id])
     VALUES
           (NULL
           ,N'FirstName'
           ,NULL
           ,N'LastName'
           ,NULL
           ,NULL
           ,CAST(N'2010-01-01 00:00:00' AS DateTime)
           ,NULL
           ,NULL
           ,NULL
           ,NULL
           ,NULL
           ,NULL
           ,NULL
           ,NULL
           ,N'{student_unique_id}'
           ,CAST(N'2021-01-01 00:00:00' AS DateTime)
           ,CAST(N'2021-01-01 00:00:00' AS DateTime)
           ,CAST('{id}' AS UNIQUEIDENTIFIER)
           )
"""
    )


def insert_edfi_student_with_usi(
    connection: Connection,
    student_usi: int,
    id: str = "00000000-0000-0000-0000-000000000000",
):
    connection.execute(
        f"""
SET IDENTITY_INSERT edfi.Student ON;

INSERT INTO [edfi].[Student]
           ([StudentUSI]
           ,[PersonalTitlePrefix]
           ,[FirstName]
           ,[MiddleName]
           ,[LastSurname]
           ,[GenerationCodeSuffix]
           ,[MaidenName]
           ,[BirthDate]
           ,[BirthCity]
           ,[BirthStateAbbreviationDescriptorId]
           ,[BirthInternationalProvince]
           ,[BirthCountryDescriptorId]
           ,[DateEnteredUS]
           ,[MultipleBirthStatus]
           ,[BirthSexDescriptorId]
           ,[CitizenshipStatusDescriptorId]
           ,[StudentUniqueId]
           ,[CreateDate]
           ,[LastModifiedDate]
           ,[Id])
     VALUES
           ({student_usi}
           ,NULL
           ,N'FirstName'
           ,NULL
           ,N'LastName'
           ,NULL
           ,NULL
           ,CAST(N'2010-01-01 00:00:00' AS DateTime)
           ,NULL
           ,NULL
           ,NULL
           ,NULL
           ,NULL
           ,NULL
           ,NULL
           ,NULL
           ,N'{student_usi}{student_usi}'
           ,CAST(N'2021-01-01 00:00:00' AS DateTime)
           ,CAST(N'2021-01-01 00:00:00' AS DateTime)
           ,CAST('{id}' AS UNIQUEIDENTIFIER)
           );

SET IDENTITY_INSERT edfi.Student OFF;
"""
    )


def insert_edfi_student_electronic_mail(
    connection: Connection,
    student_usi: int,
    email_address: str,
):
    connection.execute(
        f"""
INSERT INTO [edfi].[StudentEducationOrganizationAssociationElectronicMail]
           ([EducationOrganizationId]
           ,[ElectronicMailTypeDescriptorId]
           ,[StudentUSI]
           ,[ElectronicMailAddress]
           ,[PrimaryEmailAddressIndicator]
           ,[DoNotPublishIndicator]
           ,[CreateDate])
     VALUES
           (1
           ,1
           ,{student_usi}
           ,N'{email_address}'
           ,NULL
           ,NULL
           ,CAST(N'2021-01-01 00:00:00' AS DateTime)
           )
"""
    )


def insert_lms_section(connection: Connection, sis_identifier: str, source_system: str):
    connection.execute(
        f"""
    INSERT INTO [lms].[LMSSection]
        (
        SourceSystemIdentifier,
        SourceSystem,
        SISSectionIdentifier,
        Title,
        SourceCreateDate,
        SourceLastModifiedDate,
        CreateDate,
        LastModifiedDate)
    VALUES
        (N'{sis_identifier}'
        ,N'{source_system}'
        ,N'{sis_identifier}'
        ,N'section title'
        ,CAST(N'2021-01-01 00:00:00' AS DateTime)
        ,CAST(N'2021-01-01 00:00:00' AS DateTime)
        ,CAST(N'2021-01-01 00:00:00' AS DateTime)
        ,CAST(N'2021-01-01 00:00:00' AS DateTime)
        )
"""
    )


def insert_lms_section_deleted(
    connection: Connection, sis_identifier: str, source_system: str
):
    connection.execute(
        f"""
    INSERT INTO [lms].[LMSSection]
        (SourceSystemIdentifier,
        SourceSystem,
        SISSectionIdentifier,
        Title,
        SourceCreateDate,
        SourceLastModifiedDate,
        CreateDate,
        LastModifiedDate,
        [DeletedAt])
     VALUES
        (N'{sis_identifier}'
        ,N'{source_system}'
        ,N'{sis_identifier}'
        ,N'test section deleted'
        ,GETDATE()
        ,GETDATE()
        ,GETDATE()
        ,GETDATE()
        ,GETDATE()
        )
"""
    )


def insert_edfi_section(connection: Connection, sis_id: str, uid: str = None):
    connection.execute(
        f"""
INSERT INTO [edfi].[Section]
        (
        [LocalCourseCode],
        [SchoolId],
        [SchoolYear],
        [SessionName],
        [LastModifiedDate],
        [SectionIdentifier]
        {',[id]' if uid is not None else ''})
     VALUES
        (
        N'{COURSE_CODE}'
        ,{SCHOOL_ID}
        ,{SCHOOL_YEAR}
        ,N'{SESSION_NAME}'
        ,CAST(N'2021-01-01 00:00:00' AS DateTime2(7))
        ,N'{sis_id}'
        {f",CAST(N'{uid}' AS UNIQUEIDENTIFIER)" if uid is not None else ''}
        )
"""
    )


def insert_descriptor(connection: Connection, namespace: str, value: str):
    connection.execute(
        f"""
INSERT INTO [edfi].[Descriptor]
        (
        [Namespace],
        [CodeValue],
        [ShortDescription],
        [Description])
     VALUES
        (
            N'{namespace}',
            N'{value}',
            N'{value}',
            N'{value}'
        )
"""
    )


def insert_lmsx_sourcesystem_descriptor(connection: Connection, id: int):
    connection.execute(
        f"""
INSERT INTO [lmsx].[LMSSourceSystemDescriptor]
    (LMSSourceSystemDescriptorId)
     VALUES ( {str(id)} )
"""
    )


def insert_lmsx_assignmentcategory_descriptor(connection: Connection, id: int):
    connection.execute(
        f"""
INSERT INTO [lmsx].[AssignmentCategoryDescriptor]
    (AssignmentCategoryDescriptorId)
     VALUES ( {str(id)} )
"""
    )


def insert_lmsx_assignment(
    connection: Connection,
    assignment_id: int,
    assignment_identifier: str,
    source_system_descriptor_id: int,
    assignment_category_descriptor_id: int,
    section_identifier: str,
    title_and_description: str = "default title and description",
):
    # it is not necessary to have a different title and description since
    # both should be updated when required
    connection.execute(
        f"""
INSERT INTO [lmsx].[Assignment]
    (
        AssignmentIdentifier,
        Namespace,
        LMSSourceSystemDescriptorId,
        Title,
        AssignmentCategoryDescriptorId,
        AssignmentDescription,
        SectionIdentifier,
        LocalCourseCode,
        SessionName,
        SchoolYear
    )
     VALUES (
        N'{assignment_identifier}',
        N'Namespace',
        {source_system_descriptor_id},
        N'{title_and_description}',
        {assignment_category_descriptor_id},
        N'{title_and_description}',
        N'{section_identifier}',
        N'Local course code test',
        N'session name test',
        {SCHOOL_YEAR}
     )
"""
    )


def insert_edfi_section_association(
        connection: Connection,
        section_identifier: str,
        student_id: str):
    connection.execute(
        f"""
insert into edfi.StudentSectionAssociation (
    BeginDate,
    LocalCourseCode,
    SchoolId,
    SchoolYear,
    SectionIdentifier,
    SessionName,
    StudentUSI)
select top 1
    GETDATE() BeginDate,
    localcoursecode,
    SchoolId,
    schoolyear,
    sectionidentifier,
    sessionname,
    (select top 1 studentUSI from edfi.student where StudentUniqueId = N'{student_id}') as StudentUSI
from edfi.section
WHERE SectionIdentifier = N'{section_identifier}'
    """)


def insert_lms_assignment(
    connection: Connection,
    source_system_identifier: str,
    source_system: str,
    section_identifier: int,
    assignment_category: str,
    title_and_description: str = "default title and description",
    past_due_date: bool = False
) -> int:
    # it is not necessary to have a different title and description since
    # both should be updated when required
    connection.execute(
        f"""
INSERT INTO [lms].[Assignment]
    (
        SourceSystemIdentifier,
        SourceSystem,
        LMSSectionIdentifier,
        Title,
        AssignmentCategory,
        AssignmentDescription,
        CreateDate,
        LastModifiedDate
        { ",DueDateTime" if past_due_date else "" }
    )
     VALUES (
        N'{source_system_identifier}',
        N'{source_system}',
        {section_identifier},
        N'{title_and_description}',
        N'{assignment_category}',
        N'{title_and_description}',
        GETDATE(),
        GETDATE()
        { ",DATEADD(year, -1, GETDATE())" if past_due_date else "" }
     )
"""
    )
    result: Cursor = connection.execute("SELECT @@identity")

    return int(result.fetchone()[0])


def insert_lms_assignment_submissions(
    connection: Connection,
    lms_assignmen_identifier: int,
    source_system_identifier: str,
    lms_assignment_id: int,
    lms_user_identifier: int,
    submission_status: str,
    source_system: str = "Test_LMS",
    isDeleted: bool = False,
):
    # it is not necessary to have a different title and description since
    # both should be updated when required
    connection.execute(
        f"""
SET IDENTITY_INSERT lms.AssignmentSubmission ON;

INSERT INTO [lms].[AssignmentSubmission]
    (
        [AssignmentSubmissionIdentifier]
        ,[SourceSystemIdentifier]
        ,[SourceSystem]
        ,[AssignmentIdentifier]
        ,[LMSUserIdentifier]
        ,[SubmissionStatus]
        ,[SubmissionDateTime]
        ,[EarnedPoints]
        ,[Grade]
        ,[SourceCreateDate]
        ,[SourceLastModifiedDate]
        ,[CreateDate]
        ,[LastModifiedDate]
        ,[DeletedAt]
    )
VALUES
    (
        {lms_assignmen_identifier},
        N'{source_system_identifier}',
        N'{source_system}',
        {lms_assignment_id},
        {lms_user_identifier},
        N'{submission_status}',
        GETDATE(),
        0,
        N'{GRADE}',
        GETDATE(),
        GETDATE(),
        GETDATE(),
        GETDATE(),
        {'GETDATE()' if isDeleted else 'NULL'}
    );

SET IDENTITY_INSERT lms.AssignmentSubmission OFF;

"""
    )


def insert_lmsx_assignmentsubmissionstatus_descriptor(connection: Connection, id: int):
    connection.execute(
        f"""
INSERT INTO [lmsx].[SubmissionStatusDescriptor]
    (SubmissionStatusDescriptorId)
     VALUES ( {str(id)} )
"""
    )
