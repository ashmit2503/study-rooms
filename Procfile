release: python manage.py migrate && python manage.py collectstatic --noinput
web: gunicorn studyrooms.wsgi --log-file -
