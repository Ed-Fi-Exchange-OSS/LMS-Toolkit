IF NOT EXISTS (SELECT * FROM sys.schemas WHERE name = N'lms')
EXEC sys.sp_executesql N'CREATE SCHEMA [lms]'
GO
