release: python manage.py collectstatic --noinput
web: daphne -b 0.0.0.0 -p $PORT project.asgi:application