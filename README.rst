ODM2 Admin
==========

.. image:: https://travis-ci.org/miguelcleon/ODM2-Admin.svg?branch=master
   :target: https://travis-ci.org/miguelcleon/ODM2-Admin

This is a Django admin app for Observation Data Model 2 (ODM2). ODM2
was created through National Science Foundation Grant EAR-1224638.
Support for the development of this application comes
from NSF Grant EAR-1331841 Luquillo CZO.

Django models exist for all ODM2 tables. Forms for ODM2Core and
a number of additional ODM2 tables. Graphing of measurement result
values via highcharts are implemented. Data logger files can be
imported as long as data logger file columns and results are properly
setup.
ODM2 can be found here: https://github.com/ODM2

The file ``settings.yaml`` contains all of the database and local
file system settings which need to be configured to get a copy of this
application working. This was developed using a postgresql version of
ODM2 data model, additional modifications will be needed to make this
work with MSSQL or another database.

An example postgresql database named ODM2AdminExamplePostgresqlDB is
provided, this is a custom postgresql format backup which can be
restored to an empty database. An extrasql.sql file contains some extra
views used for efficiently exporting data as emails.


**Primary Installation**

pip install -r requirements.txt
or

# creates an env with the depepencies
conda config --add channels conda-forge --force
conda create -n ENVNAME python=2.7 --file requirements.txt

or create the conda environment with the developement requirements as well:
conda create -n ENVNAME python=2.7 --file requirements.txt --file requirements-dev.txt

# install the dependencies in the current env similar to the pip command above
conda install --file requirements.txt

You will need to run extrasql.sql on a postgreSQL instance of ODM2,
a blank schema script can be found here
(https://github.com/ODM2/ODM2/tree/master/src/blank_schema_scripts/postgresql).

**Alternate Installation - if you have issues creating the environment above
you may want to create it manually**

You might find issues with psycopg2 on windows

To install psycopg2 for windows follow the instructions here:
https://github.com/nwcell/psycopg2-windows

You may need to copy a folder from from
``C:\Users\<user name>\AppData\Local\Temp\2\pip_build_Administrator\psycopg\``
into your python library for instance
``C:\Python27\Lib\site-packages\psycopg2\``
support tested for django 1.6.5 and 1.9.x

For python 2.7
run pip install for each of these

for geoDjango you will need to install osgeo4w
https://trac.osgeo.org/osgeo4w/
https://docs.djangoproject.com/en/1.9/ref/contrib/gis/install/

psycopg2

on ubuntu apt-get install python-psycopg2

django-uuidfield https://github.com/dcramer/django-uuidfield

django-ajax-selects https://github.com/crucialfelix/django-ajax-selects

django-admin-shortcuts
https://github.com/alesdotio/django-admin-shortcuts/

djangocms\_admin\_style https://github.com/divio/djangocms-admin-style

use this version: pip install djangocms-admin-style==0.2.7

django-apptemplates https://pypi.python.org/pypi/django-apptemplates/

django-daterange-filter
https://pypi.python.org/pypi/django-daterange-filter/1.1.1

django-import-export
https://django-import-export.readthedocs.org/en/latest/installation.html

django-jquery

django-recaptcha