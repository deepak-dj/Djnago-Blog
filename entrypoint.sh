#!/bin/bash

set -e
sleep 1
python manage.py migrate
echo "migrated successfully !!!!"

if python manage.py test; then
    echo "All tests passed successfully !!!"
else
    echo "Tests failed, breaking the build!"
    exit 1
fi

echo "All test passed successfully !!!"

exec python manage.py runserver 0.0.0.0:8000
