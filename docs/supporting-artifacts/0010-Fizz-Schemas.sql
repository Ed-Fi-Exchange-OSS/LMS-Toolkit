IF NOT EXISTS (SELECT * FROM sys.schemas WHERE name = N'fizz')
EXEC sys.sp_executesql N'CREATE SCHEMA [fizz]'
GO
