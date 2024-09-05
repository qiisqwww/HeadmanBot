#!/bin/sh

psql -U $POSTGRES_USER -d $POSTGRES_DB -f /docker-entrypoint-initdb.d/migrations/migration_create_base_tables.sql
psql -U $POSTGRES_USER -d $POSTGRES_DB -f /docker-entrypoint-initdb.d/migrations/migration_new_value_to_role_enum.sql
psql -U $POSTGRES_USER -d $POSTGRES_DB -f /docker-entrypoint-initdb.d/migrations/migration_added_nstu_uni_enum.sql