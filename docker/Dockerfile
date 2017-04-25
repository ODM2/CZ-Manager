FROM continuumio/miniconda:latest

ENV LANG=C.UTF-8 LC_ALL=C.UTF-8

LABEL description='Django admin app for Observation Data Model 2 (ODM2)' \
      url='https://github.com/miguelcleon/ODM2-Admin' \
      author='Miguel Leon' \
      author_email='leonmi@sas.upenn.edu' \
      development_status='5 - Production/Stable' \
      environment='Console' \
      intended_audience='Science/Research, Developers, Education' \
      license='MIT License' \
      operating_system='OS Independent' \
      programming_language='Python' \
      topic='Scientific/Engineering, Education'

EXPOSE 8010
EXPOSE 5432

VOLUME /db

# Setting up postgresql database
RUN apt-get update --fix-missing && apt-get install -y postgresql postgresql-client postgresql-contrib postgis

RUN git clone "https://github.com/miguelcleon/ODM2-Admin"


RUN cd ODM2-Admin && latest=$(git describe --tags) && git checkout ${latest}

RUN service postgresql start && su - postgres -c 'psql -U postgres -c "create database odm2_db"'

# RUN service postgresql start && su - postgres -c 'psql -U postgres -c "create database odm2_db"' && \
#    su - postgres -c 'pg_restore -d odm2_db -1 -v "/ODM2-Admin/ODM2AdminExamplePostgresqlDB"' && \
#    su - postgres -c "psql -U postgres -d postgres -c \"alter user postgres with password 'test';\"" 

# creates an env with the depepencies
RUN conda create --yes -n odm2adminenv -c conda-forge python=2.7 pytz gdal --file /ODM2-Admin/requirements.txt
RUN update-rc.d postgresql enable

COPY development.py /ODM2-Admin/templatesAndSettings/settings/
COPY entrypoint.sh /
COPY startup.sh /

RUN chmod 755 /entrypoint.sh
RUN chmod 755 /startup.sh

CMD ["/bin/bash", "entrypoint.sh", "startup.sh"]
