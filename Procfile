web: python manage.py migrate && gunicorn FutureFarm.wsgi
celeryBeatWorker: celery -A FutureFarm worker & celery -A FutureFarm beat --loglevel=info
