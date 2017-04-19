# ODM2Admin Docker Image Creation

Requirements to run [docker image](https://hub.docker.com/r/lsetiawan/odm2admin/):

1. ODM2 Database backup sql for PostgreSQL called odm2admindb.backup.
2. Docker installed on Linux or MacOS, currently not working on windows.
To run:
$ docker run -d -p 8010:8010 -v /path/to/local/db/backup/folder/:/db/ lsetiawan/odm2admin:latest