
# ODM2 Admin
This is a Django admin app for Observation Data Model 2 (ODM2). ODM2 was created through National Science Foundation Grant EAR-1224638.

Django models exist for all ODM2 tables. Forms for ODM2Core and some additional tables have been created. Graphing of measurement result values via highcharts are implemented. Data logger files can be imported as long as data logger file columns and results are properly setup.   
ODM2 can be found here: https://github.com/ODM2

In the folder templatesAndSettings you will find settings.py which contains all of the database and local file system settings which need to be configured to get a copy of this application working. This was developed using a postgresql version of ODM2 data model, additional modifications will be needed to make this work with MSSQL or another database. 

You might find issues with psycopg2 on windows 

To install psycopg2 for windows follow the instructions here:  
https://github.com/nwcell/psycopg2-windows

You may need to copy a folder from from C:\Users\<user name>\AppData\Local\Temp\2\pip_build_Administrator\psycopg\ into your python library for instance C:\Python27\Lib\site-packages\psycopg2\ 

support tested for django 1.6.5 and 1.9.x

python 2.7
run pip install for each of these

psycopg2 

on ubuntu apt-get install python-psycopg2

django-uuidfield https://github.com/dcramer/django-uuidfield

django-ajax-selects https://github.com/crucialfelix/django-ajax-selects

django-admin-shortcuts https://github.com/alesdotio/django-admin-shortcuts/

djangocms_admin_style https://github.com/divio/djangocms-admin-style

use this version: pip install djangocms-admin-style==0.2.7 

django-apptemplates https://pypi.python.org/pypi/django-apptemplates/

django-daterange-filter https://pypi.python.org/pypi/django-daterange-filter/1.1.1

django-import-export https://django-import-export.readthedocs.org/en/latest/installation.html

django-jquery 
