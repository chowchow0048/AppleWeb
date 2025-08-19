web: cd appleWeb && gunicorn config.wsgi:application -c ../gunicorn.conf.py
release: cd appleWeb && python manage.py collectstatic --noinput && python manage.py migrate 