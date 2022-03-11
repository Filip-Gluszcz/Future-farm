web: python manage.py migrate && gunicorn FutureFarm.wsgi
worker: celery -A FutureFarm worker --loglevel=info
beat: celery -A FutureFarm beat --loglevel=info
celeryworker: celery -A FutureFarm worker & celery -A FutureFarm worker --loglevel=info & wait -n