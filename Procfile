web: sh -c "python manage.py migrate --noinput && gunicorn event_project.wsgi:application --log-file - --bind 0.0.0.0:$PORT"
