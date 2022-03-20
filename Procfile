web: python manage.py migrate && gunicorn FutureFarm.wsgi
worker: celery -A FutureFarm worker --loglevel=info
beat: celery -A FutureFarm beat --loglevel=info
celeryWorker: celery -A FutureFarm worker & celery -A FutureFarm beat --loglevel=info & wait -n
celeryBeatWorkerConcurrency: celery -A FutureFarm worker & celery -A FutureFarm beat --loglevel=info --concurrency=1
celeryBeatWorker: celery -A FutureFarm worker & celery -A FutureFarm beat --loglevel=info