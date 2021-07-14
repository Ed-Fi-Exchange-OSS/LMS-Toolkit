IF NOT EXISTS (SELECT * FROM sys.schemas WHERE name = N'lmsx')
EXEC sys.sp_executesql N'CREATE SCHEMA [lmsx]'
GO
