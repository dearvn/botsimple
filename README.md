# Information
This package to build bot trading simple with thousand requests using rabbitmq, redis and docker

## Installation to test on local not use docker
```bash

# Create an isolated Python virtual environment
pip3 install virtualenv
virtualenv ./virtualenv --python=$(which python3)

# Activate the virtualenv
# IMPORTANT: it needs to be activated every time before you run
. virtualenv/bin/activate

# Install Python requirements
pip install -r requirements.txt

# Install cointrol-*
pip install -e ./app
```

## Run on server
```bash
# Build docker
docker pull rabbitmq:latest 
docker-compose build
docker-compose run

# Run api choose options, I will build cmnd in docker-compose later
# Use Api from django
docker exec -i -t botsimple_app_1  /bin/bash
python manage.py runserver 0.0.0.0:8000

#or
flask run

## Scale
# Can scale multi-dockers
docker-compose scale worker=5
