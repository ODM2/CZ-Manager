.. _Managing-ODM2-With-The-Django-ORM:

The Django ORM and WOFpy
========================

While not all of the ODM2 entities are exposed through the CZ Manager interface they can all be managed using Python
scripts using either ODM2PythonAPI or the Django ORM using the models in CZ Manager. Two examples using the Django ORM
 are included with the source code of CZ Manager.

The ODM2PythonAPI can be found here: https://github.com/ODM2/ODM2PythonAPI

An example of merging data from a csv file to  fill a gap in a time series can be found here:
https://github.com/ODM2/CZ-Manager/blob/master/example_scripts/SonadoraNitrateFill.py

An example creating soil profile result values from a file can be found here:
https://github.com/ODM2/CZ-Manager/tree/master/soilsIngestionExample

WOFpy
-----

CZ Manager can also be used with WOFpy and water one flow webservices can be registered with CUAHSI HIS central.

WOFpy REST API test page for the Luquillo CZO:
http://odm2admin.cuahsi.org/odm2lczo/odm2lczo/rest_1_1/

This is still in testing an initial implementation has been registered with the HIS central QA system:

http://qa-hiscentral.cuahsi.org/testpage.aspx?n=100002

QA HIS client:

http://qa-hiswebclient.azurewebsites.net/

* :ref:`CZ Manager docs home page<ODM2-Admin>`
* :ref:`Search the docs <search>`