# ODM2-Admin Docker Application

Before proceeding below, make sure that you have [Docker](https://docs.docker.com/engine/installation/) and [Docker Compose](https://docs.docker.com/compose/install/) installed.


To deploy this application on Docker simply navigate to current directory `docker-deploy`.

Execute docker-compose to deploy the application:

```bash
# OSX/Windows, used sudo for Linux
docker-compose up
```

Check that ODM2Admin is now running by going to: http://127.0.0.1:8000/

Once the application is running, open another terminal and create super user by executing the command below.

```bash
# OSX/Windows, used sudo for Linux
docker exec -it odm2adminapp /opt/conda/envs/odm2adminenv/bin/python manage.py createsuperuser
```

