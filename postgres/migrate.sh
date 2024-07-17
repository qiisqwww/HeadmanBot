#!/bin/sh

psql -U root -d root -f postgres/migrations/migration_create_base_tables.sql
psql -U root -d root -f postgres/migrations/migration_new_value_to_role_enum.sql