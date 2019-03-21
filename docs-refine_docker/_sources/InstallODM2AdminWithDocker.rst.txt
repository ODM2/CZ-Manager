ODM2 Admin Docker Image Creation
================================

Requirements to run [docker image](https://cloud.docker.com/repository/docker/miguelcleon/odm2-admin):

1. Docker installed on Linux, MacOS, or Windows.

To run:

.. code:: bash

   $ docker run -d -p 8010:8010 --name odm2admintest miguelcleon/odm2-admin:latest

Next, in order to login you will need to create a Django superuser login
To do that first you will need to attach bash to the container, then
activate the conda environment in the container, change directories to
the folder containing the application and run the manage.py createsuperuser
command.

.. code:: bash

   $ docker exec -it odm2admintest /bin/bash
   $ source activate odm2adminenv
   $ python /ODM2-Admin/manage.py createsuperuser


follow the interactive prompt, once complete you will be able to login through
a web browser at 127.0.0.1:8010 with your new account.

* :ref:`ODM2 Admin docs home page<ODM2-Admin>`
* :ref:`Search the docs <search>`