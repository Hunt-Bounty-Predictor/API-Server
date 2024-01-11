#!/bin/sh
# wait-for-postgres.sh

set -e

host="$1"

export POSTGREWS_PASSWORD=password
export POSTGRES_USER=happy
export POSTGRES_DB=hunt

until PGPASSWORD=$POSTGRES_PASSWORD psql -h "$host" -U "$POSTGRES_USER" -d "$POSTGRES_DB" -c '\q'; do
  >&2 echo "Postgres is unavailable - sleeping"
  sleep 1
done
