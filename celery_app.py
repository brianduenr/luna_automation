from celery import Celery
import os

redis_url = os.environ.get('REDIS_URL', 'redis://localhost:6379/0')

app = Celery('tasks',
             broker=redis_url,
             backend=redis_url,
             include=['tasks'])

if __name__ == '__main__':
    app.start()
