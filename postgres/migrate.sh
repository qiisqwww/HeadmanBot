#!/bin/sh

for file in "/docker-entrypoint-initdb.d/migrations"/*.sql; do
    psql -U $POSTGRES_USER -d $POSTGRES_DB -f $file;
done
