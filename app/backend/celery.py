import os

from celery import Celery

from .tasks import YoutubeScraping

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')

app = Celery('backend')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()


@app.task
def scraping(settings: dict):
    youtube_scraping = YoutubeScraping(settings=settings)
    youtube_scraping.youtube_search()
