#!/bin/sh
echo "Waiting for PostgreSQL to be ready..."
until nc -zv -w30 ${DB_HOST} ${DB_PORT}
do
  echo "Waiting for database connection"
  sleep 10
done

echo "PostgreSQL is up - running migrations..."

flask --app app db upgrade
python run.py
