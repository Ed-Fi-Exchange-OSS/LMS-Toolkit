ALTER TABLE edfilms.Assignment ADD CONSTRAINT FK_153cda_AssignmentCategoryDescriptor FOREIGN KEY (AssignmentCategoryDescriptorId)
REFERENCES edfilms.AssignmentCategoryDescriptor (AssignmentCategoryDescriptorId)
;

CREATE INDEX FK_153cda_AssignmentCategoryDescriptor
ON edfilms.Assignment (AssignmentCategoryDescriptorId ASC);

ALTER TABLE edfilms.Assignment ADD CONSTRAINT FK_153cda_Section FOREIGN KEY (LocalCourseCode, SchoolId, SchoolYear, SectionIdentifier, SessionName)
REFERENCES edfi.Section (LocalCourseCode, SchoolId, SchoolYear, SectionIdentifier, SessionName)
ON UPDATE CASCADE
;

CREATE INDEX FK_153cda_Section
ON edfilms.Assignment (LocalCourseCode ASC, SchoolId ASC, SchoolYear ASC, SectionIdentifier ASC, SessionName ASC);

ALTER TABLE edfilms.Assignment ADD CONSTRAINT FK_153cda_SourceSystemDescriptor FOREIGN KEY (SourceSystemDescriptorId)
REFERENCES edfi.SourceSystemDescriptor (SourceSystemDescriptorId)
;

CREATE INDEX FK_153cda_SourceSystemDescriptor
ON edfilms.Assignment (SourceSystemDescriptorId ASC);

ALTER TABLE edfilms.AssignmentCategoryDescriptor ADD CONSTRAINT FK_b35549_Descriptor FOREIGN KEY (AssignmentCategoryDescriptorId)
REFERENCES edfi.Descriptor (DescriptorId)
ON DELETE CASCADE
;

ALTER TABLE edfilms.AssignmentSubmission ADD CONSTRAINT FK_f12526_Assignment FOREIGN KEY (AssignmentIdentifier)
REFERENCES edfilms.Assignment (AssignmentIdentifier)
;

CREATE INDEX FK_f12526_Assignment
ON edfilms.AssignmentSubmission (AssignmentIdentifier ASC);

ALTER TABLE edfilms.AssignmentSubmission ADD CONSTRAINT FK_f12526_Student FOREIGN KEY (StudentUSI)
REFERENCES edfi.Student (StudentUSI)
;

CREATE INDEX FK_f12526_Student
ON edfilms.AssignmentSubmission (StudentUSI ASC);

ALTER TABLE edfilms.AssignmentSubmission ADD CONSTRAINT FK_f12526_SubmissionStatusDescriptor FOREIGN KEY (SubmissionStatusDescriptorId)
REFERENCES edfilms.SubmissionStatusDescriptor (SubmissionStatusDescriptorId)
;

CREATE INDEX FK_f12526_SubmissionStatusDescriptor
ON edfilms.AssignmentSubmission (SubmissionStatusDescriptorId ASC);

ALTER TABLE edfilms.AssignmentSubmissionType ADD CONSTRAINT FK_6f15e4_Assignment FOREIGN KEY (AssignmentIdentifier)
REFERENCES edfilms.Assignment (AssignmentIdentifier)
ON DELETE CASCADE
;

CREATE INDEX FK_6f15e4_Assignment
ON edfilms.AssignmentSubmissionType (AssignmentIdentifier ASC);

ALTER TABLE edfilms.AssignmentSubmissionType ADD CONSTRAINT FK_6f15e4_SubmissionTypeDescriptor FOREIGN KEY (SubmissionTypeDescriptorId)
REFERENCES edfilms.SubmissionTypeDescriptor (SubmissionTypeDescriptorId)
;

CREATE INDEX FK_6f15e4_SubmissionTypeDescriptor
ON edfilms.AssignmentSubmissionType (SubmissionTypeDescriptorId ASC);

ALTER TABLE edfilms.SubmissionStatusDescriptor ADD CONSTRAINT FK_8e9244_Descriptor FOREIGN KEY (SubmissionStatusDescriptorId)
REFERENCES edfi.Descriptor (DescriptorId)
ON DELETE CASCADE
;

ALTER TABLE edfilms.SubmissionTypeDescriptor ADD CONSTRAINT FK_ddc450_Descriptor FOREIGN KEY (SubmissionTypeDescriptorId)
REFERENCES edfi.Descriptor (DescriptorId)
ON DELETE CASCADE
;

