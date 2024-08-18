#!/bin/sh

sudo docker-compose -f /opt/HeadmanBot/docker/docker-compose.yml --env-file /var/www/HeadmanBot/.env/.env up --build
