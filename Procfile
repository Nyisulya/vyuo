web: gunicorn vyuofinder.wsgi:application
release: python manage.py migrate && python manage.py create_default_admin
