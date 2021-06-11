IF NOT EXISTS (SELECT * FROM sys.schemas WHERE name = N'edfilms')
EXEC sys.sp_executesql N'CREATE SCHEMA [edfilms]'
GO
