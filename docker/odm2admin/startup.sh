#!/bin/bash

set -e

echo "Activating environment..."
source activate odm2adminenv
# pip install git+git://github.com/miguelcleon/django-admin-shortcuts --upgrade

#echo "Building database..."
#su - postgres -c 'pg_restore -d odm2_db -1 -v "/ODM2-Admin/ODM2AdminDBBlank"'
#
#su - postgres -c "psql -U postgres -d postgres -c \"alter user postgres with password 'test';\""
#
echo "Migrate django tables"
python manage.py migrate

echo "Loading Controlled Vocabularies"
python /cvload.py postgresql+psycopg2://$POSTGRES_USER:$POSTGRES_PASSWORD@$POSTGRES_HOST:$POSTGRES_PORT/$POSTGRES_NAME

echo "Running server..."
python manage.py runserver 0.0.0.0:8000
