from celery import shared_task

from .get_caption import GetCaption
from .get_list import GetVideoList


@shared_task
def get_list(settings: dict):
    youtube_scraping = GetVideoList(settings=settings)
    youtube_scraping.get_video_list()


@shared_task
def get_caption(data: dict):
    caption = GetCaption(data=data)
    caption.get_caption()
