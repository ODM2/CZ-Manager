#!/bin/bash

echo "Activating environment..."
source activate odm2adminenv

echo "Building database..."
su - postgres -c 'pg_restore -d odm2_db -1 -v "/ODM2-Admin/ODM2AdminDBBlank"'

su - postgres -c "psql -U postgres -d postgres -c \"alter user postgres with password 'test';\""

echo "Migrate django tables"
python /ODM2-Admin/manage.py migrate

echo "Running server..."
python /ODM2-Admin/manage.py runserver 0.0.0.0:8010