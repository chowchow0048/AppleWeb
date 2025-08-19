web: cd appleWeb && python manage.py collectstatic --noinput && gunicorn config.wsgi:application -c ../gunicorn.conf.py
release: cd appleWeb && python manage.py migrate --noinput 