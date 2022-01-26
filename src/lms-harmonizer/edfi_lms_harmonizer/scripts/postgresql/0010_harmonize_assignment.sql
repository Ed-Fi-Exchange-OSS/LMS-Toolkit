-- SPDX-License-Identifier: Apache-2.0
-- Licensed to the Ed-Fi Alliance under one or more agreements.
-- The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
-- See the LICENSE and NOTICES files in the project root for more information.

create or replace procedure lms.harmonize_assignment(_sourcesystem varchar(255), _namespace varchar(255))
as $$
begin

    create extension if not exists "pgcrypto";

	create temp table all_assignments as
	select
		lmsassignment.sourcesystemidentifier as assignmentidentifier,
		sourcesystemdescriptor.descriptorid as lmssourcesystemdescriptorid,
		lmsassignment.title,
		assignmentcatdescriptor.descriptorid as assignmentcategorydescriptorid,
		lmsassignment.assignmentdescription,
		lmsassignment.startdatetime,
		lmsassignment.enddatetime,
		lmsassignment.duedatetime,
		lmsassignment.maxpoints,
		edfisection.sectionidentifier,
		edfisection.localcoursecode,
		edfisection.sessionname,
		edfisection.schoolyear,
		edfisection.schoolid,
		lmsassignment.lastmodifieddate as assignment_last_modified_date,
		lmssection.deletedat as section_deleted,
		lmsassignment.deletedat as assignment_deleted
 	from lms.assignment lmsassignment
		inner join lms.lmssection lmssection
			on lmsassignment.lmssectionidentifier = lmssection.lmssectionidentifier

		inner join edfi.section edfisection
			on lmssection.edfisectionid = edfisection.id

		inner join edfi.descriptor sourcesystemdescriptor
			on sourcesystemdescriptor.codevalue = lmsassignment.sourcesystem

		inner join lmsx.lmssourcesystemdescriptor
		    on sourcesystemdescriptor.descriptorid  = lmssourcesystemdescriptor.lmssourcesystemdescriptorid

		inner join edfi.descriptor assignmentcatdescriptor
			on assignmentcatdescriptor.codevalue = lmsassignment.assignmentcategory
			and assignmentcatdescriptor.namespace = 'uri://ed-fi.org/edfilms/AssignmentCategoryDescriptor/' || _sourcesystem

		inner join lmsx.assignmentcategorydescriptor
			on assignmentcatdescriptor.descriptorid = assignmentcategorydescriptor.assignmentcategorydescriptorid

    where lmsassignment.sourcesystem = _sourcesystem;

	insert into lmsx.assignment
		(assignmentidentifier
		,lmssourcesystemdescriptorid
		,title
		,assignmentcategorydescriptorid
		,assignmentdescription
		,startdatetime
		,enddatetime
		,duedatetime
		,maxpoints
		,sectionidentifier
		,localcoursecode
		,sessionname
		,schoolyear
		,schoolid
		,namespace
        ,id
        )
	select
		assignmentidentifier
		,lmssourcesystemdescriptorid
		,title
		,assignmentcategorydescriptorid
		,assignmentdescription
		,startdatetime
		,enddatetime
		,duedatetime
		,maxpoints
		,sectionidentifier
		,localcoursecode
		,sessionname
		,schoolyear
		,schoolid
		,_namespace
        ,(select gen_random_uuid()::uuid)
	from
	all_assignments
	where
		all_assignments.assignmentidentifier not in (
            select assignmentidentifier from lmsx.assignment
        )
		and
			section_deleted is null
		and
			assignment_deleted is null;


	update lmsx.assignment
	set
		title = all_assignments.title,
		assignmentcategorydescriptorid = all_assignments.assignmentcategorydescriptorid,
		assignmentdescription = all_assignments.assignmentdescription,
		startdatetime = all_assignments.startdatetime,
		enddatetime = all_assignments.enddatetime,
		duedatetime = all_assignments.duedatetime,
		maxpoints = all_assignments.maxpoints,
		lastmodifieddate = now()
	from
		all_assignments
	where
		lmsx.assignment.assignmentidentifier = all_assignments.assignmentidentifier
		and
			all_assignments.assignment_last_modified_date > lmsx.assignment.lastmodifieddate;


	delete from lmsx.assignmentsubmission
		where lmsx.assignmentsubmission.assignmentidentifier in (
            select assignmentidentifier from all_assignments where assignment_deleted is not null
        );


	delete from lmsx.assignment
		where lmsx.assignment.assignmentidentifier in (
            select assignmentidentifier from all_assignments where assignment_deleted is not null
        );

    drop table all_assignments;

end;

$$ language plpgsql;
