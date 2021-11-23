# Docker directory

Contains docker-compose file for starting up SQL Server or PostgreSQL, useful
for local testing of the LMS-DS-Loader and LMS-Harmonizer if you don't have
these two installed.

To get started, copy the `.env.example` file to `.env` and modify as
appropriate. Make sure that you modify the `.env` files for the applications
(LMS-DS-Loader, LMS-Harmonizer) appropriately so that they have matching
settings.
