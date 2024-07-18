#!/bin/bash

set -e
echo "Starting the deployment process..."

echo "Step 1: Running migrations..."
sleep 1
python manage.py migrate
echo "Migrated successfully !!!!"

echo "Step 2: Running tests..."
if python manage.py test; then
    echo "All tests passed successfully !!!"
else
    echo "Tests failed, breaking the build!"
    exit 1
fi

echo "Step 3: Starting the application..."
exec python manage.py runserver 0.0.0.0:8000
