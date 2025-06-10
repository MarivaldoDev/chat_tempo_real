web: daphne -b 0.0.0.0 -p $PORT project.asgi:application
release: python manage.py migrate && python manage.py collectstatic --noinput