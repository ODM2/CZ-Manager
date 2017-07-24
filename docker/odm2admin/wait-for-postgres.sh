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

psql -v ON_ERROR_STOP=1 --host "$host" --username "postgres" -c "CREATE DATABASE odm2;"
psql -v ON_ERROR_STOP=1 --host "$host" --username "postgres" --dbname "odm2" --file /odm2adminDB.sql

>&2 echo "Postgres is up - executing command"
exec $cmd