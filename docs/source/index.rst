ODM2 Admin
==========
.. C:\Python27\Scripts\sphinx-build.exe "C:\Users\leonmi\Google Drive\ODM2AdminLT3\docs\source" "C:\Users\leonmi\Google Drive\ODM2AdminLT3\docs\build"
   run sphinx

This is an app for site level data management using Observation Data Model 2 (ODM2). ODM2
was created through National Science Foundation Grant EAR-1224638.
Support for the development of this application comes
from NSF Grant EAR-1331841 Luquillo CZO.

ODM2 can be found here: https://github.com/ODM2

Other ODM2 tools can be used in conjunction with ODM2 Admin, extensive
testing has been done using ODM2 Admin with ODM2PythonAPI and WOFpy.

Django ORM models exist for all ODM2 tables. Forms for ODM2Core and
a number of additional ODM2 tables. Sites are mapped via a leaflet mapping interface.
Graphing of time series result values via highcharts are implemented.
Data logger files can be imported with properly configured data logger file columns and
time series results results.

Diagram of ODM2 Admin infrastructure:
-------------------------------------

.. image:: /images/ODM2AdminInfrastructure.png


The file ``settings.yaml`` contains all of the database and local
file system settings which need to be configured to get a copy of this
application working. This was developed using a postgresql version of
ODM2 data model, additional modifications will be needed to make this
work with MSSQL or another database.

An example postgresql database named ODM2AdminExamplePostgresqlDB is
provided, this is a custom postgresql format backup which can be
restored to an empty database. An extrasql.sql file contains some extra
views used for efficiently exporting data as emails.


Primary Installation
--------------------

The fastest way to get started is to install with DockerHub:

.. toctree::
   :maxdepth: 1

   InstallODM2AdminWithDocker

Alternatively you can download the source code from github (https://github.com/ODM2/ODM2-Admin) setup a conda
environment, create an ODM2 database, run the extrasql.sql script (found in the root directory of the source code)
on that database, and change settings in:

ODM2-Admin-master\templatesAndSettings\settings\base.py
ODM2-Admin-master\templatesAndSettings\settings\development.py

When your depolying to production you will want to change the settings in production.py instead of development.py
You can also have the settings files point to an existing ODM2 database, you will need to run the extrasql.sql on
the database.

.. code:: bash

  pip install -r requirements.txt

or

.. code:: bash

  conda config --add channels conda-forge --force
  conda create -n ENVNAME python=2.7 --file requirements.txt

or create the conda environment with the development requirements as well:

.. code:: bash

  conda create -n ENVNAME python=2.7 --file requirements.txt --file requirements-dev.txt --channel conda-forge

You will need to run ``extrasql.sql`` on a postgreSQL instance of ODM2,
a blank schema script can be found here:
https://github.com/ODM2/ODM2/tree/master/src/blank_schema_scripts/postgresql

Using ODM2 Admin
==================
The documents below provide instructions on using ODM2 Admin.

.. toctree::
   :maxdepth: 1

   GettingStartedInODM2Admin
   ODM2AdminShortcuts

