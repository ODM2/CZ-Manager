# ODM2Admin Docker Image Creation

Requirements to run [docker image](https://hub.docker.com/r/lsetiawan/odm2admin/):

1. Docker installed on Linux, MacOS, or Windows.

To run:
$ docker run -d -p 8010:8010 --name odm2admintest lsetiawan/odm2admin:latest

Next, in order to login you will need to create a Django superuser login
To do that first you will need to attach bash to the container, then
activate the conda environment in the container, change directories to
the folder containing the application and run the manage.py createsuperuser
command. 
$ docker exec -it odm2admintest /bin/bash
$ source activate odm2adminenv
$ cd ODM2-Admin
$ python manage.py createsuperuser

follow the interactive prompt, once complete you will be able to login through
a web browser at 0.0.0.0:8010 with your new account.