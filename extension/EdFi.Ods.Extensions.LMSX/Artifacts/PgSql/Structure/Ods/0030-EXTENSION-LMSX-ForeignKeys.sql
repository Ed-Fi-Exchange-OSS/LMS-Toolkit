ALTER TABLE lmsx.Assignment ADD CONSTRAINT FK_153cda_AssignmentCategoryDescriptor FOREIGN KEY (AssignmentCategoryDescriptorId)
REFERENCES lmsx.AssignmentCategoryDescriptor (AssignmentCategoryDescriptorId)
;

CREATE INDEX FK_153cda_AssignmentCategoryDescriptor
ON lmsx.Assignment (AssignmentCategoryDescriptorId ASC);

ALTER TABLE lmsx.Assignment ADD CONSTRAINT FK_153cda_LMSSourceSystemDescriptor FOREIGN KEY (LMSSourceSystemDescriptorId)
REFERENCES lmsx.LMSSourceSystemDescriptor (LMSSourceSystemDescriptorId)
;

CREATE INDEX FK_153cda_LMSSourceSystemDescriptor
ON lmsx.Assignment (LMSSourceSystemDescriptorId ASC);

ALTER TABLE lmsx.Assignment ADD CONSTRAINT FK_153cda_School FOREIGN KEY (SchoolId)
REFERENCES edfi.School (SchoolId)
;

CREATE INDEX FK_153cda_School
ON lmsx.Assignment (SchoolId ASC);

ALTER TABLE lmsx.Assignment ADD CONSTRAINT FK_153cda_Section FOREIGN KEY (LocalCourseCode, SchoolId, SchoolYear, SectionIdentifier, SessionName)
REFERENCES edfi.Section (LocalCourseCode, SchoolId, SchoolYear, SectionIdentifier, SessionName)
ON UPDATE CASCADE
;

CREATE INDEX FK_153cda_Section
ON lmsx.Assignment (LocalCourseCode ASC, SchoolId ASC, SchoolYear ASC, SectionIdentifier ASC, SessionName ASC);

ALTER TABLE lmsx.AssignmentCategoryDescriptor ADD CONSTRAINT FK_b35549_Descriptor FOREIGN KEY (AssignmentCategoryDescriptorId)
REFERENCES edfi.Descriptor (DescriptorId)
ON DELETE CASCADE
;

ALTER TABLE lmsx.AssignmentSubmission ADD CONSTRAINT FK_f12526_Assignment FOREIGN KEY (AssignmentIdentifier, SchoolId)
REFERENCES lmsx.Assignment (AssignmentIdentifier, SchoolId)
;

CREATE INDEX FK_f12526_Assignment
ON lmsx.AssignmentSubmission (AssignmentIdentifier ASC, SchoolId ASC);

ALTER TABLE lmsx.AssignmentSubmission ADD CONSTRAINT FK_f12526_Student FOREIGN KEY (StudentUSI)
REFERENCES edfi.Student (StudentUSI)
;

CREATE INDEX FK_f12526_Student
ON lmsx.AssignmentSubmission (StudentUSI ASC);

ALTER TABLE lmsx.AssignmentSubmission ADD CONSTRAINT FK_f12526_SubmissionStatusDescriptor FOREIGN KEY (SubmissionStatusDescriptorId)
REFERENCES lmsx.SubmissionStatusDescriptor (SubmissionStatusDescriptorId)
;

CREATE INDEX FK_f12526_SubmissionStatusDescriptor
ON lmsx.AssignmentSubmission (SubmissionStatusDescriptorId ASC);

ALTER TABLE lmsx.AssignmentSubmissionType ADD CONSTRAINT FK_6f15e4_Assignment FOREIGN KEY (AssignmentIdentifier, SchoolId)
REFERENCES lmsx.Assignment (AssignmentIdentifier, SchoolId)
ON DELETE CASCADE
;

CREATE INDEX FK_6f15e4_Assignment
ON lmsx.AssignmentSubmissionType (AssignmentIdentifier ASC, SchoolId ASC);

ALTER TABLE lmsx.AssignmentSubmissionType ADD CONSTRAINT FK_6f15e4_SubmissionTypeDescriptor FOREIGN KEY (SubmissionTypeDescriptorId)
REFERENCES lmsx.SubmissionTypeDescriptor (SubmissionTypeDescriptorId)
;

CREATE INDEX FK_6f15e4_SubmissionTypeDescriptor
ON lmsx.AssignmentSubmissionType (SubmissionTypeDescriptorId ASC);

ALTER TABLE lmsx.LMSSourceSystemDescriptor ADD CONSTRAINT FK_d263fc_Descriptor FOREIGN KEY (LMSSourceSystemDescriptorId)
REFERENCES edfi.Descriptor (DescriptorId)
ON DELETE CASCADE
;

ALTER TABLE lmsx.SubmissionStatusDescriptor ADD CONSTRAINT FK_8e9244_Descriptor FOREIGN KEY (SubmissionStatusDescriptorId)
REFERENCES edfi.Descriptor (DescriptorId)
ON DELETE CASCADE
;

ALTER TABLE lmsx.SubmissionTypeDescriptor ADD CONSTRAINT FK_ddc450_Descriptor FOREIGN KEY (SubmissionTypeDescriptorId)
REFERENCES edfi.Descriptor (DescriptorId)
ON DELETE CASCADE
;

