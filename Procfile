web: gunicorn --worker-class eventlet -w 1 --bind 0.0.0.0:$PORT app:app
worker: celery -A celery_app worker --loglevel=info
