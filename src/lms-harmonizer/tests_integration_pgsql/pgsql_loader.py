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
    insert into lms.lmsuser
           (sourcesystemidentifier
           ,sourcesystem
           ,userrole
           ,sisuseridentifier
           ,localuseridentifier
           ,name
           ,emailaddress
           ,sourcecreatedate
           ,sourcelastmodifieddate
           ,createdate
           ,lastmodifieddate
           ,deletedat)
     values
           ('{sis_identifier}'
           ,'{source_system}'
           ,'{USER_ROLE}'
           ,'{sis_identifier}1'
           ,'{sis_identifier}2'
           ,'{sis_identifier}3'
           ,'{email_address}'
           ,NULL
           ,NULL
           ,'2021-01-01 00:00:00'
           ,'2021-01-01 00:00:00'
           ,NULL
           )
"""
    )


def insert_lms_user_deleted(
    connection: Connection, sis_identifier: str, email_address: str, source_system: str
):
    connection.execute(
        f"""
    insert into lms.lmsuser
           (sourcesystemidentifier
           ,sourcesystem
           ,userrole
           ,sisuseridentifier
           ,localuseridentifier
           ,name
           ,emailaddress
           ,sourcecreatedate
           ,sourcelastmodifieddate
           ,createdate
           ,lastmodifieddate
           ,deletedat)
     values
           ('{sis_identifier}'
           ,'{source_system}'
           ,'{USER_ROLE}'
           ,'{sis_identifier}1'
           ,'{sis_identifier}2'
           ,'{sis_identifier}3'
           ,'{email_address}'
           ,NULL
           ,NULL
           ,'2021-01-01 00:00:00'
           ,'2021-01-01 00:00:00'
           ,'2021-01-02 00:00:00'
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
insert into edfi.student
           (personaltitleprefix
           ,firstname
           ,middlename
           ,lastsurname
           ,generationcodesuffix
           ,maidenname
           ,birthdate
           ,birthcity
           ,birthstateabbreviationdescriptorid
           ,birthinternationalprovince
           ,birthcountrydescriptorid
           ,dateenteredus
           ,multiplebirthstatus
           ,birthsexdescriptorid
           ,citizenshipstatusdescriptorid
           ,studentuniqueid
           ,createdate
           ,lastmodifieddate
           ,id)
     values
           (NULL
           ,'FirstName'
           ,NULL
           ,'LastName'
           ,NULL
           ,NULL
           ,'2010-01-01 00:00:00'
           ,NULL
           ,NULL
           ,NULL
           ,NULL
           ,NULL
           ,NULL
           ,NULL
           ,NULL
           ,'{student_unique_id}'
           ,'2021-01-01 00:00:00'
           ,'2021-01-01 00:00:00'
           ,'{id}'
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
insert into edfi.student
           (studentusi
           ,personaltitleprefix
           ,firstname
           ,middlename
           ,lastsurname
           ,generationcodesuffix
           ,maidenname
           ,birthdate
           ,birthcity
           ,birthstateabbreviationdescriptorid
           ,birthinternationalprovince
           ,birthcountrydescriptorid
           ,dateenteredus
           ,multiplebirthstatus
           ,birthsexdescriptorid
           ,citizenshipstatusdescriptorid
           ,studentuniqueid
           ,createdate
           ,lastmodifieddate
           ,id)
overriding system value
     values
           ({student_usi}
           ,NULL
           ,'FirstName'
           ,NULL
           ,'LastName'
           ,NULL
           ,NULL
           ,'2010-01-01 00:00:00'
           ,NULL
           ,NULL
           ,NULL
           ,NULL
           ,NULL
           ,NULL
           ,NULL
           ,NULL
           ,'{student_usi}{student_usi}'
           ,'2021-01-01 00:00:00'
           ,'2021-01-01 00:00:00'
           ,'{id}'
           );
"""
    )


def insert_edfi_student_electronic_mail(
    connection: Connection,
    student_usi: int,
    email_address: str,
):
    connection.execute(
        f"""
insert into edfi.studenteducationorganizationassociationelectronicmail\
           (educationorganizationid
           ,electronicmailtypedescriptorid
           ,studentusi
           ,electronicmailaddress
           ,primaryemailaddressindicator
           ,donotpublishindicator
           ,createdate)
     values
           (1
           ,1
           ,{student_usi}
           ,'{email_address}'
           ,NULL
           ,NULL
           ,'2021-01-01 00:00:00'
           )
"""
    )


def insert_lms_section(connection: Connection, sis_identifier: str, source_system: str):
    connection.execute(
        f"""
    insert into lms.lmssection
        (
        sourcesystemidentifier,
        sourcesystem,
        sissectionidentifier,
        title,
        sourcecreatedate,
        sourcelastmodifieddate,
        createdate,
        lastmodifieddate)
    values
        ('{sis_identifier}'
        ,'{source_system}'
        ,'{sis_identifier}'
        ,'section title'
        ,'2021-01-01 00:00:00'
        ,'2021-01-01 00:00:00'
        ,'2021-01-01 00:00:00'
        ,'2021-01-01 00:00:00'
        )
"""
    )


def insert_lms_section_deleted(
    connection: Connection, sis_identifier: str, source_system: str
):
    connection.execute(
        f"""
    insert into lms.lmssection
        (sourcesystemidentifier,
        sourcesystem,
        sissectionidentifier,
        title,
        sourcecreatedate,
        sourcelastmodifieddate,
        createdate,
        lastmodifieddate,
        deletedat)
     values
        ('{sis_identifier}'
        ,'{source_system}'
        ,'{sis_identifier}'
        ,'test section deleted'
        ,now()
        ,now()
        ,now()
        ,now()
        ,now()
        )
"""
    )


def insert_edfi_section(connection: Connection, sis_id: str, uid: str = None):
    connection.execute(
        f"""
insert into edfi.section
        (
        localcoursecode,
        schoolid,
        schoolyear,
        sessionname,
        lastmodifieddate,
        sectionidentifier
        ,id)
     values
        (
        '{COURSE_CODE}'
        ,{SCHOOL_ID}
        ,{SCHOOL_YEAR}
        ,'{SESSION_NAME}'
        ,'2021-01-01 00:00:00'
        ,'{sis_id}'
        {f",{uid}" if uid is not None else ",(select md5(random()::text || random()::text)::uuid)"}
        )
"""
    )


def insert_descriptor(connection: Connection, namespace: str, value: str):
    connection.execute(
        f"""
insert into edfi.descriptor
        (
        namespace,
        codevalue,
        shortdescription,
        description,
        id)
     values
        (
            '{namespace}',
            '{value}',
            '{value}',
            '{value}',
            (select md5(random()::text || random()::text)::uuid)
        )
"""
    )


def insert_lmsx_sourcesystem_descriptor(connection: Connection, id: int):
    connection.execute(
        f"""
insert into lmsx.lmssourcesystemdescriptor
    (lmssourcesystemdescriptorid)
     values ( {str(id)} )
"""
    )


def insert_lmsx_assignmentcategory_descriptor(connection: Connection, id: int):
    connection.execute(
        f"""
insert into lmsx.assignmentcategorydescriptor
    (assignmentcategorydescriptorid)
     values ( {str(id)} )
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
insert into lmsx.assignment
    (
        assignmentidentifier,
        namespace,
        lmssourcesystemdescriptorid,
        title,
        assignmentcategorydescriptorid,
        assignmentdescription,
        sectionidentifier,
        localcoursecode,
        sessionname,
        schoolyear
    )
     values (
        '{assignment_identifier}',
        'Namespace',
        {source_system_descriptor_id},
        '{title_and_description}',
        {assignment_category_descriptor_id},
        '{title_and_description}',
        '{section_identifier}',
        'Local course code test',
        'session name test',
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
insert into edfi.studentsectionassociation (
    begindate,
    localcoursecode,
    schoolid,
    schoolyear,
    sectionidentifier,
    sessionname,
    studentusi)
select top 1
    now() begindate,
    localcoursecode,
    schoolid,
    schoolyear,
    sectionidentifier,
    sessionname,
    (select top 1 studentusi from edfi.student where studentuniqueid = '{student_id}') as studentusi
from edfi.section
where sectionidentifier = '{section_identifier}'
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
insert into lms.assignment
    (
        sourcesystemidentifier,
        sourcesystem,
        lmssectionidentifier,
        title,
        assignmentcategory,
        assignmentdescription,
        createdate,
        lastmodifieddate
        { ",duedatetime" if past_due_date else "" }
    )
     values (
        '{source_system_identifier}',
        '{source_system}',
        {section_identifier},
        '{title_and_description}',
        '{assignment_category}',
        '{title_and_description}',
        now(),
        now()
        { ",now() - interval '1 year'" if past_due_date else "" }
     )
"""
    )
    result: Cursor = connection.execute("select lastval()")

    return int(result.fetchone()[0])


def insert_lms_assignment_submissions(
    connection: Connection,
    lms_assignment_identifier: int,
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
insert into lms.assignmentsubmission
    (
        assignmentsubmissionidentifier
        ,sourcesystemidentifier
        ,sourcesystem
        ,assignmentidentifier
        ,lmsuseridentifier
        ,submissionstatus
        ,submissiondatetime
        ,earnedpoints
        ,grade
        ,sourcecreatedate
        ,sourcelastmodifieddate
        ,createdate
        ,lastmodifieddate
        ,deletedat
    )
overriding system value
values
    (
        {lms_assignment_identifier},
        '{source_system_identifier}',
        '{source_system}',
        {lms_assignment_id},
        {lms_user_identifier},
        '{submission_status}',
        now(),
        0,
        '{GRADE}',
        now(),
        now(),
        now(),
        now(),
        {'now()' if isDeleted else 'NULL'}
    );
"""
    )


def insert_lmsx_assignmentsubmissionstatus_descriptor(connection: Connection, id: int):
    connection.execute(
        f"""
insert into lmsx.submissionstatusdescriptor
    (submissionstatusdescriptorid)
     values ( {str(id)} )
"""
    )
