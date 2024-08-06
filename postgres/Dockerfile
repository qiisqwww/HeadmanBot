FROM postgres:16.3-alpine3.20


COPY postgresql.conf /etc/postgresql/
COPY migrate.sh /docker-entrypoint-initdb.d
COPY migrations /docker-entrypoint-initdb.d/migrations/

CMD ["postgres", "-c", "config_file=/etc/postgresql/postgresql.conf"]
