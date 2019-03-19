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

RUN apt-get update --fix-missing && apt-get install --yes apt-utils postgresql-client

EXPOSE 8000

# && latest=$(git describe --tags) && git checkout ${latest}
RUN git clone "https://github.com/ODM2/ODM2-Admin"
RUN cd ODM2-Admin


WORKDIR /ODM2-Admin

VOLUME templatesAndSettings/settings/

RUN conda create --yes -n odm2adminenv -c conda-forge python=3.6 libgdal boost pytz gdal --file requirements.txt

COPY odm2database/odm2adminDB.sql /odm2adminDB.sql
COPY odm2database/cvload.py /cvload.py

COPY wait-for-postgres.sh /wait-for-postgres.sh
COPY startup.sh /startup.sh

RUN chmod 755 /wait-for-postgres.sh
RUN chmod 755 /startup.sh

CMD ["/bin/bash", "/wait-for-postgres.sh", "db", "/startup.sh"]
