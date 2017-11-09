ODM2 Admin
==========

.. image:: https://travis-ci.org/ODM2/ODM2-Admin.svg?branch=master
   :target: https://travis-ci.org/ODM2/ODM2-Admin

This is a Django admin app for Observation Data Model 2 (ODM2). ODM2
was created through National Science Foundation Grant EAR-1224638.
Support for the development of this application comes
from NSF Grant EAR-1331841 Luquillo CZO.

ODM2 can be found here: https://github.com/ODM2

Django models exist for all ODM2 tables. Forms for ODM2Core and
a number of additional ODM2 tables. Graphing of measurement result
values via highcharts are implemented. Data logger files can be
imported as long as data logger file columns and results are properly
setup.


Other ODM2 tools can be used in conjunction with ODM2 Admin, extensive
testing has been done using ODM2 Admin with ODM2PythonAPI and WOFpy.

This was developed using a postgresql version of
ODM2 data model, additional modifications may be needed to make this
work with MSSQL or another database.

An example postgresql database named ODM2AdminExamplePostgresqlDB is
provided, this is a custom postgresql format backup which can be
restored to an empty database. An extrasql.sql file contains some extra
views used for efficiently exporting data as emails.



**Primary Installation**
See Docker Folder for dockerhub installation instructions or

see http://odm2.github.io/ODM2-Admin/ for local installation instructions.