from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.utils.datetime_safe import datetime


class Word(models.Model):
    word_ini = models.CharField(max_length=1)
    word = models.CharField(max_length=50, unique=True)
    word_imi = models.CharField(max_length=120, default='default')

    def __str__(self):
        return self.word


class Caption(models.Model):
    video_href = models.CharField(max_length=10)
    index = models.IntegerField()
    href_index = models.CharField(max_length=20,
                                  default=str(video_href) + f'[{index}]',
                                  unique=True,
                                  editable=False)
    start_time = models.IntegerField()
    end_time = models.IntegerField()
    text = models.CharField(max_length=100)
    word = ArrayField(models.CharField(max_length=20))
    word_imi = ArrayField(models.CharField(max_length=20))

    def __str__(self):
        num = self.index
        return self.video_href + f'[{num}]'


class Video(models.Model):
    video_href = models.CharField(max_length=10, unique=True)
    video_img = models.CharField(max_length=20)
    video_time = models.CharField(max_length=10)
    video_title = models.CharField(max_length=50)
    video_genre = ArrayField(models.CharField(max_length=20))
    youtubeID = models.CharField(max_length=20)
    video_upload_date = models.DateTimeField()

    def __str__(self):
        return self.video_href
