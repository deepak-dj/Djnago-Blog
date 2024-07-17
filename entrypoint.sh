#!/bin/bash

sleep 1
python manage.py migrate
echo "migrated successfully !!!!"

python manage.py test
echo "All test passed successfully !!!"

exec python manage.py runserver 0.0.0.0:8000
