#!/bin/bash

set -e
cd /app_vpn

postgres_ready(){
python << END
import sys
import psycopg2
try:
    conn = psycopg2.connect(dbname="$DB_NAME", user="$DB_USER", password="$DB_PASSWORD", host="$DB_HOST", port="5432")
except psycopg2.OperationalError:
    sys.exit(-1)
sys.exit(0)
END
}

echo "Waiting for Postgres..."
until postgres_ready; do
  echo "Postgres is unavailable - sleeping"
  sleep 1
done
echo "Postgres is up - continuing..."

echo "Install dep..."
pip install -r conf/requirements.txt

echo "Running collectstatic..."
python manage.py collectstatic --noinput

echo "Running migrations..."
python manage.py migrate

echo "Running server..."
python manage.py runserver 0.0.0.0:8000

tail -f /dev/null