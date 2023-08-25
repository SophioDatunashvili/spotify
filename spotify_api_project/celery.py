import os

from celery import Celery
from celery.schedules import crontab

from datetime import timedelta, datetime

os.environ.setdefault("DJANGO_SETTINGS_MODULE", 'spotify_api_project.settings')

app = Celery('spotify_api_project')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

from spotify_api_client.tasks import fetch_and_store_new_releases

# Trigger the task immediately when Celery starts
fetch_and_store_new_releases.apply_async(eta=datetime.now() + timedelta(seconds=1))

app.conf.beat_schedule = {
		'fetch-new-releases-later': {
			'task': 'spotify_api_client.tasks.fetch_and_store_new_releases',
			'schedule': crontab(minute=0, hour=0),  # Run every 24 hours
			'args': (),  # No additional arguments
		},
	}
#
# @app.task(bind=True, ignore_result=True)
# def debug_task(self):
# 	print(f'Request: {self.request!r}')
