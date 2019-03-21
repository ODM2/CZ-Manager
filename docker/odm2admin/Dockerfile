FROM continuumio/miniconda:latest

ENV LANG=C.UTF-8 LC_ALL=C.UTF-8
ENV APP_PATH /usr/src/app

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

SHELL ["/bin/bash", "-c"]

RUN apt-get update --fix-missing && apt-get install --yes apt-utils wget postgresql-client

EXPOSE 8000

WORKDIR ${APP_PATH}

COPY . ${APP_PATH}

RUN wget -O /cvload.py https://raw.githubusercontent.com/ODM2/ODM2/master/src/load_cvs/cvload.py

RUN conda create --yes -n odm2adminenv -c conda-forge python=3.6 libgdal boost pytz gdal sqlalchemy pymysql pyodbc --file requirements.txt

COPY docker/odm2admin/odm2database/odm2adminDB.sql /odm2adminDB.sql

COPY docker/odm2admin/wait-for-postgres.sh /wait-for-postgres.sh
COPY docker/odm2admin/startup.sh /startup.sh

RUN chmod 755 /wait-for-postgres.sh
RUN chmod 755 /startup.sh

CMD ["/bin/bash", "/wait-for-postgres.sh", "/startup.sh"]
