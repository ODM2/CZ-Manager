#!/bin/bash
# wait-for-postgres.sh

set -e

host="$1"
shift
cmd="$@"

until psql -h "$host" -U "postgres" -c '\l'; do
  >&2 echo "Postgres is unavailable - sleeping"
  sleep 1
done



# sql to check whether given database exist
sql1="select count(1) from pg_catalog.pg_database where datname = 'odm2'"

# depending on how PATH is set psql may require a fully qualified path
cmd="psql -h \"$host\" -U \"postgres\" -t -c \"$sql1\""

db_exists=`eval $cmd`

if [ $db_exists -eq 0 ] ; then
   # create the database, discard the output
   >&2 echo " create odm2 db 1 time "
   psql -v ON_ERROR_STOP=1 --host "$host" --username "postgres" -c "CREATE DATABASE odm2;"
   eval $cmd
fi


# psql -v ON_ERROR_STOP=1 --host "$host" --username "postgres" -c "CREATE DATABASE odm2;"
psql -v ON_ERROR_STOP=1 --host "$host" --username "postgres" --dbname "odm2" --file /odm2adminDB.sql

>&2 echo "Postgres is up - executing command"
exec $cmd