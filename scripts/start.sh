#!/bin/sh

sudo docker-compose -f /var/www/HeadmanBot/docker/docker-compose.yml --env-file /var/www/HeadmanBot/.env/.env up --build
