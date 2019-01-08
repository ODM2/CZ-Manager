.. _ODM2-Admin:

ODM2 Admin
==========
.. C:\Python27\Scripts\sphinx-build.exe "C:\Users\leonmi\Google Drive\ODM2AdminLT3\docs\source" "C:\Users\leonmi\Google Drive\ODM2AdminLT3\docs\build"
   run sphinx

ODM2 Admin is an application for site level data management of environmental observations using
Observation Data Model 2 (ODM2). The application was designed for management of data from the Luquillo
Critical Zone Observatory located in northeastern Puerto Rico. For more details about why ODM2 Admin was developed
see :ref:`Motivation-for-ODM2-Admin`

ODM2 was created through National Science Foundation Grant EAR-1224638.
Support for the development of this application comes from NSF Grant EAR-1331841 Luquillo CZO.

The ODM2 Admin source code can be found here: https://github.com/ODM2/ODM2-Admin

ODM2 can be found here: https://github.com/ODM2

Other ODM2 tools can be used in conjunction with ODM2 Admin, extensive
testing has been done using ODM2 Admin with ODM2PythonAPI and WOFpy.

Django ORM models exist for all ODM2 tables. Web forms for ODM2Core and
a number of additional ODM2 tables. Sites and sampling features are mapped via a leaflet mapping interface.
Graphing of time series result values via highcharts are implemented.
Data logger files can be imported with properly configured data logger file columns and
time series results results.

Diagram of ODM2 Admin infrastructure:
-------------------------------------

.. image:: /images/ODM2AdminInfrastructure.png

ODM2 Admin was initially developed using a postgresql version of the ODM2 data model. ODM2 Admin has also been used with
Microsoft SQL and SQLite implementations of ODM2.

Extended infrasructure with WOFpy web services and ODM2PythonAPI
----------------------------------------------------------------

.. image:: /images/Extendedinfrastructure.png

ODM2 Admin can be setup in conjunction with WOFpy and ODM2PythonAPI. WOFpy implements CUAHSI's water one flow web
services. See the `WOFpy github page <https://github.com/ODM2/WOFpy>`_ for more.
ODM2PythoAPI is a A Python-based application programmer's interface for the Observations Data Model 2 (ODM2).
For more see the `ODM2PythonAPI github page <https://github.com/ODM2/ODM2PythonAPI>`_

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

.. code:: bash

   ODM2-Admin-master\templatesAndSettings\settings\base.py
   ODM2-Admin-master\templatesAndSettings\settings\development.py

When you are depolying to production you will want to change the settings in production.py instead of development.py
You can also have the settings files point to an existing ODM2 database, you will need to run the extrasql.sql on
the database. For more details on settings see :ref:`ODM2-Admin-Settings`

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

Six instances of ODM2 Admin have been deployed and are hosted by CUAHSI. If you are interested in an ODM2 Admin
instance, hosted on the CUAHSI cloud, contact leonmi@sas.upenn.edu

* http://odm2admin.cuahsi.org/LCZO/mapdata.html
* http://odm2admin.cuahsi.org/DryCreek/mapdata.html
* http://odm2admin.cuahsi.org/TRACE/TRACE/mapdata.html
* http://odm2admin.cuahsi.org/CJCZO/mapdata.html
* http://msu-odm2admin.cuahsi.org/MSU/mapdata.html
* https://odm2admin.cuahsi.org/CZIMEA/mapdata.html

.. image:: /images/CUAHSI-Logo-with-URL---Transparent_(RESIZED).png

Another deployment for demonstration porposes is available, see the :ref:'ODM2AdminDemo' for more
information:

http://odm2admin.cuahsi.org/Sandbox/

Using ODM2 Admin
================
The documents below provide instructions on using ODM2 Admin.

.. toctree::
   :maxdepth: 1

   Motivation for ODM2 Admin <ODM2Adminbackground>
   GettingStartedInODM2Admin
   configuring ODM2 Admin Settings <ODM2AdminSettings>




ODM2 Admin Walkthrough
======================
The ODM2 Admin Walkthrough uses a Sandbox instance of ODM2 Admin while also documenting the work through steps
with detailed descriptions and images from the sandbox. Many of the features of ODM2 Admin are described here.

.. toctree::
   :maxdepth: 1

   ODM2 Admin Walkthrough <ODM2AdminDemo>


* :ref:`ODM2-Administration`
* :ref:`Using Data Logger Files <DataLoggerFiles>`
* :ref:`Managing Profile Results With ODM2 Admin <ProfileResults>`
* :ref:`Time series QA/QC <Data-QA-QC>`
* :ref:`Data Sharing and Visualization Tips <Data-Visualization>`
* :ref:`Managing ODM2 With The Django ORM <Managing-ODM2-With-The-Django-ORM>`

Docs Home
---------
* :ref:`ODM2 Admin docs home page <ODM2-Admin>`
* :ref:`Search the docs <search>`