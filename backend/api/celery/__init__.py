from __future__ import absolute_import, unicode_literals

# This will make sure the api is always imported when
# Django starts so that shared_task will use this api.
from .celery import app as celery_app

__all__ = ("celery_app",)
