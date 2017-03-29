#!/bin/bash

echo "Activating environment..."
source activate odm2adminenv

echo "Building database..."
su - postgres -c 'pg_restore -d odm2_db -1 -v "/db/odm2admindb.backup"'
su - postgres -c "psql -U postgres -d postgres -c \"alter user postgres with password 'test';\""

echo "Running server..."
python /ODM2-Admin/manage.py runserver 0.0.0.0:8010