# ODM2Admin Docker

To run build and run the ODM2Admin docker, ensure you have the latest docker and docker-compose.

1. Go to the root repo and run the command below.

``` bash
docker-compose -f docker/docker-deploy/docker-compose.yml up --build
```

Next, in order to login you will need to create a Django superuser login
To do that first you will need to attach bash to the container, then
activate the conda environment in the container, change directories to
the folder containing the application and run the manage.py createsuperuser
command.

```bash
# On local terminal
docker exec -it odm2adminapp /bin/bash

# On docker container terminal
source activate odm2adminenv
python /ODM2-Admin/manage.py createsuperuser
```

follow the interactive prompt, once complete you will be able to login through
a web browser at http://127.0.0.1:8000 with your new account.