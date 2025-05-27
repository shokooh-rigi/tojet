#!/bin/bash

# Wait for the database to be ready
echo "Waiting for the database to be ready..."
while ! nc -z postgres_db 5432; do
  sleep 1
done

# Run migrations
echo "Running makemigrations..."
python /app/manage.py makemigrations
python /app/manage.py migrate --noinput
echo "Database migrations complete."

echo "Collecting static files..."
python /app/manage.py collectstatic --noinput
echo "Static files collected."

# Start the Django server
echo "Starting Django server..."
if [ "DEBUG" = "FALSE" ]; then
    echo "Starting Gunicorn server..."
    exec gunicorn --workers=4 --bind 0.0.0.0:8000 tojet.wsgi:application
else
    echo "Starting Django development server..."
    exec python /app/manage.py runserver 0.0.0.0:8000
fi
