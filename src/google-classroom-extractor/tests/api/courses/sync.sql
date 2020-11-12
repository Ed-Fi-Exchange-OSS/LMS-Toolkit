-- Create Courses table
CREATE TABLE IF NOT EXISTS Courses (
	id BIGINT, 
	name TEXT, 
	section BIGINT, 
	descriptionHeading TEXT, 
	description TEXT, 
	room TEXT, 
	ownerId BIGINT, 
	creationTime TEXT, 
	updateTime TEXT, 
	enrollmentCode BIGINT, 
	courseState TEXT, 
	alternateLink TEXT, 
	teacherGroupEmail TEXT, 
	courseGroupEmail TEXT, 
	guardiansEnabled BOOLEAN, 
	calendarId BIGINT, 
	Hash TEXT, 
	SyncNeeded BIGINT,
	CreateDate DATETIME,
	LastModifiedDate DATETIME,
	PRIMARY KEY (id)
);

CREATE INDEX SYNCNEEDED_INDEX ON Courses(SyncNeeded);


-- differing by hash - see https://www.mysqltutorial.org/compare-two-tables-to-find-unmatched-records-mysql.aspx/
-- single entry in result set if id only exists in one table (meaning add or missing), so SyncNeeded flag will indicate which table it's from
-- double entry in result set if id exists in both (meaning update needed), so SyncNeeded will show which row is from which table
CREATE TABLE UnmatchedTable AS
  SELECT * FROM (
	SELECT * FROM Courses
	UNION ALL
	SELECT * FROM Temp_Courses
  )
  GROUP BY id, Hash 
  HAVING COUNT(*) = 1;

CREATE INDEX ID_INDEX ON UnmatchedTable(id);
--

DROP TABLE UnmatchedTable
--


-- all rows start with CreateDate and LastModifiedDate initialized to now by Python
-- but updated rows instead need the original CreateDate pulled from existing table

-- Note: UPDATE-FROM is not available in sqlite until v3.33.0, thus the goofiness
UPDATE UnmatchedTable
	SET CreateDate = (
		SELECT c.CreateDate
        FROM Courses c
        WHERE c.id = UnmatchedTable.id
    )
	WHERE EXISTS (
		SELECT *
        FROM Courses c
        WHERE c.id = UnmatchedTable.id
	) AND SyncNeeded = 1
	
	
-- update DataFrame with the changed record CreateDate updates
SELECT id, CreateDate
FROM UnmatchedTable
	WHERE id IN (
	    SELECT id FROM UnmatchedTable
	    GROUP BY id
	    HAVING COUNT(*) > 1
	) AND SyncNeeded = 1


-- deletes and inserts next	
	
WITH
    -- changed rows CTE (from SyncNeeded side only)
	changedRows AS (
		SELECT * FROM UnmatchedTable
		WHERE id IN (
		    SELECT id FROM UnmatchedTable
		    GROUP BY id
		    HAVING COUNT(*) > 1
		) AND SyncNeeded = 1
	),
	
	-- new rows CTE (of course from SyncNeeded side)
	newRows AS (
		SELECT * FROM UnmatchedTable
		WHERE id IN (
		    SELECT id FROM UnmatchedTable
		    GROUP BY id
		    HAVING COUNT(*) = 1 AND SyncNeeded = 1
		)
	)


-- delete the obsolete data
DELETE FROM Courses
WHERE id IN (
	SELECT id from changedRows
)

-- insert new and changed data
INSERT INTO Courses
	SELECT * FROM UnmatchedTable
	WHERE id IN (
		SELECT id FROM changedRows
		UNION ALL
		SELECT id FROM newRows
	) AND SyncNeeded = 1

	
-- reset SyncNeeded flag on main table
UPDATE Courses
SET SyncNeeded = 0
WHERE SyncNeeded != 0


