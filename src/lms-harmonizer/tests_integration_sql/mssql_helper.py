# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.
from os import path
from sqlalchemy.engine.base import Connection
from edfi_lms_harmonizer.helpers.argparser import MainArguments


def _script_path(script_name: str) -> str:
    return path.normpath(
        path.join(
            path.dirname(__file__),
            "..",
            "..",
            "..",
            "extension",
            "EdFi.Ods.Extensions.EdFiLMS",
            "Artifacts",
            "MsSql",
            "Structure",
            "Ods",
            script_name,
        )
    )


def script_sql(script_name: str) -> str:
    script = open(_script_path(script_name), "r")
    result = script.read()
    script.close()
    return result


def main_arguments() -> MainArguments:
    args = MainArguments(log_level="INFO")
    args.set_connection_string_using_integrated_security(
        "localhost", 1433, "test_harmonizer_lms_toolkit"
    )
    return args


def insert_lms_user(connection: Connection, sis_identifier: str, source_system: str):
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
           ,N'student'
           ,N'{sis_identifier}'
           ,N'{sis_identifier}'
           ,N'{sis_identifier}'
           ,N'{sis_identifier}'
           ,NULL
           ,NULL
           ,CAST(N'2021-01-01 00:00:00' AS DateTime)
           ,CAST(N'2021-01-01 00:00:00' AS DateTime)
           ,NULL
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


def insert_edfi_student_identification_code(
    connection: Connection,
    student_usi: int,
    identification_code: str,
):
    connection.execute(
        f"""
INSERT INTO [edfi].[StudentEducationOrganizationAssociationStudentIdentificationCode]
           ([AssigningOrganizationIdentificationCode]
           ,[EducationOrganizationId]
           ,[StudentIdentificationSystemDescriptorId]
           ,[StudentUSI]
           ,[IdentificationCode]
           ,[CreateDate])
     VALUES
           (N'{identification_code}'
           ,1
           ,2
           ,{student_usi}
           ,N'{identification_code}'
           ,CAST(N'2021-01-01 00:00:00' AS DateTime)
           )
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
