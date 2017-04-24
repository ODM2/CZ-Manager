#!/bin/bash

echo "Activating environment..."
source activate odm2adminenv
conda install --yes -c conda-forge pytz

echo "Building database..."

su - postgres -c 'pg_restore -d odm2_db -1 -v "/ODM2-Admin/ODM2AdminExamplePostgresqlDB"'

su - postgres -c "psql -U postgres -d postgres -c \"alter user postgres with password 'test';\""

echo "Running server..."
python /ODM2-Admin/manage.py runserver 0.0.0.0:8010