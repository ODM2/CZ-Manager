#!/bin/bash
set -e

cmd="$1"

service postgresql start

until su - postgres -c "psql -U postgres -w -c '\l'"; do
  >&2 echo "Postgres is unavailable - sleeping"
  sleep 10
done

>&2 echo "Postgres is up - executing command"
exec bash $cmd