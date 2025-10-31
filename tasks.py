from celery_app import app
import asyncio
from main import run_automation

@app.task(bind=True)
def run_automation_task(self, input_csv, output_csv, luna_url, wake_word):
    def log_to_celery(message):
        self.update_state(state='PROGRESS', meta={'log': message})

    asyncio.run(run_automation(input_csv, output_csv, luna_url, wake_word, logger=log_to_celery))
