-- SPDX-License-Identifier: Apache-2.0
-- Licensed to the Ed-Fi Alliance under one or more agreements.
-- The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
-- See the LICENSE and NOTICES files in the project root for more information.

create or replace procedure lms.harmonize_assignment_submissions(_sourcesystem varchar(255), _namespace varchar(255))
as $$
declare begin

    create extension if not exists "pgcrypto";

	create temp table all_submissions on commit drop as
	select
		lmssubmission.sourcesystemidentifier,
		edfistudent.studentusi,
		lmsxassignment.assignmentidentifier,
		submissionstatusdescriptor.descriptorid,
		lmssubmission.submissiondatetime,
		lmssubmission.earnedpoints,
		lmssubmission.grade,
		lmssubmission.createdate,
		lmssubmission.lastmodifieddate,
		lmssubmission.deletedat
	from
		lms.assignmentsubmission as lmssubmission
	inner join
		lms.assignment as lmsassignment
	on
		lmssubmission.assignmentidentifier = lmsassignment.assignmentidentifier
	inner join
		lmsx.assignment as lmsxassignment
	on
		lmsassignment.sourcesystemidentifier = lmsxassignment.assignmentidentifier
	inner join lms.lmsuser lmsuser
		on lmsuser.lmsuseridentifier = lmssubmission.lmsuseridentifier
	inner join edfi.descriptor submissionstatusdescriptor
		on submissionstatusdescriptor.codevalue = lmssubmission.submissionstatus
		and submissionstatusdescriptor.namespace = 'uri://ed-fi.org/edfilms/SubmissionStatusDescriptor/' || lmssubmission.sourcesystem
    inner join lmsx.submissionstatusdescriptor lmsxsubmissionstatus
        on submissionstatusdescriptor.descriptorid = lmsxsubmissionstatus.submissionstatusdescriptorid
	inner join edfi.student edfistudent
		on edfistudent.id = lmsuser.edfistudentid
    where lmssubmission.sourcesystem = _sourcesystem;

	if _sourcesystem = 'Schoology'
	then
		insert into all_submissions
		select distinct
			format(
				'%s#%s#%s',
				lmssection.sourcesystemidentifier,
				lmsxassignment.assignmentidentifier,
				lmsstudent.sourcesystemidentifier
			) as sourcesystemidentifier,
			edfisectionassociation.studentusi,
			lmsxassignment.assignmentidentifier,
			case when lmsxassignment.duedatetime < now() then
				latesubmissionstatusdescriptor.descriptorid
			else
				upcomingsubmissionstatusdescriptor.descriptorid
			end,
			null::timestamp as submissiondatetime,
			null::integer as earnedpoints,
			null as grade,
			now() as createdate,
			now() as lastmodifieddate,
			null::timestamp as deletedat

		from edfi.studentsectionassociation edfisectionassociation
		inner join lmsx.assignment lmsxassignment
			on edfisectionassociation.sectionidentifier = lmsxassignment.sectionidentifier
		inner join lms.assignment lmsassignment
			on lmsassignment.sourcesystemidentifier = lmsxassignment.assignmentidentifier
		inner join edfi.student edfistudent
			on edfistudent.studentusi = edfisectionassociation.studentusi
		inner join lms.lmsuser lmsstudent
			on lmsstudent.edfistudentid = edfistudent.id
		inner join edfi.section edfisection
			-- The LMS Harmonizer requires that SectionIdentifier be unique, thus it is
			-- safe in this scenario to ignore the other natural key elements in this join.
			on edfisection.sectionidentifier = edfisectionassociation.sectionidentifier
		inner join lms.lmssection lmssection
			on lmssection.edfisectionid = edfisection.id
		inner join lateral (
			select
				submissionstatusdescriptor.descriptorid
			from
				edfi.descriptor submissionstatusdescriptor
			where
				submissionstatusdescriptor.namespace = 'uri://ed-fi.org/edfilms/SubmissionStatusDescriptor/' || _sourcesystem
			and
				submissionstatusdescriptor.codevalue = 'missing'
		) as latesubmissionstatusdescriptor on true
		inner join lateral (
			select
				submissionstatusdescriptor.descriptorid
			from
				edfi.descriptor submissionstatusdescriptor
			where
				submissionstatusdescriptor.namespace = 'uri://ed-fi.org/edfilms/SubmissionStatusDescriptor/' || _sourcesystem
			and
				submissionstatusdescriptor.codevalue = 'Upcoming'
		) as upcomingsubmissionstatusdescriptor on true
		where not exists (
			select 1 from lms.assignmentsubmission lmssubmission where lmssubmission.assignmentidentifier = lmsassignment.assignmentidentifier
				and lmssubmission.lmsuseridentifier = lmsstudent.lmsuseridentifier
		)
		and (edfisectionassociation.enddate is null or edfisectionassociation.enddate > lmsassignment.duedatetime)
		and lmsassignment.sourcesystem = _sourcesystem;
	end if;

	insert into lmsx.assignmentsubmission(
		assignmentsubmissionidentifier,
		studentusi,
		assignmentidentifier,
		namespace,
		submissionstatusdescriptorid,
		submissiondatetime,
		earnedpoints,
		grade,
        id
	)
	select
        sourcesystemidentifier,
        studentusi,
        assignmentidentifier,
        _namespace,
        descriptorid,
        submissiondatetime,
        earnedpoints,
        grade,
        (select gen_random_uuid()::uuid)
    from all_submissions
    where
    not exists (
        select 1 from lmsx.assignmentsubmission where assignmentsubmissionidentifier = all_submissions.sourcesystemidentifier
    )
    and
        all_submissions.deletedat is null;


	update lmsx.assignmentsubmission set
		submissionstatusdescriptorid = all_submissions.descriptorid,
		submissiondatetime = all_submissions.submissiondatetime,
		earnedpoints = all_submissions.earnedpoints,
		grade = all_submissions.grade,
		lastmodifieddate = now()
	from all_submissions
	where all_submissions.sourcesystemidentifier = lmsx.assignmentsubmission.assignmentsubmissionidentifier
	and all_submissions.lastmodifieddate > lmsx.assignmentsubmission.lastmodifieddate
	and all_submissions.deletedat is null;

	delete from lmsx.assignmentsubmission
	where lmsx.assignmentsubmission.assignmentsubmissionidentifier in
		(select lmssubmission.sourcesystemidentifier from lms.assignmentsubmission lmssubmission where lmssubmission.deletedat is not null);

end;

$$ language plpgsql;
