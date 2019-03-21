#!/bin/bash
# wait-for-postgres.sh

set -e
cmd="$@"

until PGPASSWORD=$POSTGRES_PASSWORD psql -h "$POSTGRES_HOST" -U "$POSTGRES_USER" -c '\l'; do
  echo >&2 "$(date +%Y-%m-%dT%H-%M-%S) Postgres is unavailable - sleeping"
  sleep 1
done

until psql -h "$POSTGRES_HOST" -U "$POSTGRES_USER" -c "SELECT 1 AS result FROM pg_database
WHERE datname='$POSTGRES_NAME'" | grep -qw 1 ; do
  echo >&2 "$(date +%Y-%m-%dT%H-%M-%S) $POSTGRES_NAME is unavailable"
  psql -v ON_ERROR_STOP=1 --host "$POSTGRES_HOST" --username "$POSTGRES_USER" -c "CREATE DATABASE $POSTGRES_NAME;"
  sleep 1
done
echo >&2 "$(date +%Y-%m-%dT%H-%M-%S) $POSTGRES_NAME has been created"


# psql -v ON_ERROR_STOP=1 --host "$host" --username "postgres" -c "CREATE DATABASE odm2;"
psql -v ON_ERROR_STOP=1 --host "$POSTGRES_HOST" --username "$POSTGRES_USER" --dbname "$POSTGRES_NAME" --file /odm2adminDB.sql

>&2 echo "Postgres is up - executing command"
exec $cmd