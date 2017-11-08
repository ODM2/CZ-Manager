ODM2 Admin
==========

This is a Django admin app for Observation Data Model 2 (ODM2). ODM2
was created through National Science Foundation Grant EAR-1224638.
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


Primary Installation
--------------------

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


.. toctree::
   :maxdepth: 2
   :caption: Contents:



Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
