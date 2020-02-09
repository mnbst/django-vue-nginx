from django.db import models
from django.contrib.postgres.fields import ArrayField


class Word(models.Model):
    word_ini = models.CharField(max_length=1)
    word = models.CharField(max_length=50, unique=True)
    word_imi = models.CharField(max_length=120, default='default')

    def __str__(self):
        return self.word


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


class Caption(models.Model):
    video_href = models.ForeignKey(Video,
                                   to_field='video_href',
                                   on_delete=models.CASCADE)
    index = models.IntegerField(default=0)
    start_time = models.IntegerField(default=0)
    end_time = models.IntegerField(default=0)
    text = models.CharField(max_length=100)
    word = ArrayField(models.CharField(max_length=20))
    word_imi = ArrayField(
        models.CharField(max_length=20, null=True, blank=True))

    def __str__(self):
        return self.video_href + f'[{self.index}]'


class FetchSetting(models.Model):
    authority = models.CharField(max_length=30, default="super", unique=True)
    excepted_href = ArrayField(models.CharField(max_length=20),
                               default=list,
                               null=True,
                               blank=True)
    page_to_crawl = models.IntegerField(default=5)
    language_limit = models.IntegerField(default=1)
    minimum_sentence = models.IntegerField(default=10)
    video_to_delete = ArrayField(models.CharField(max_length=20),
                                 default=list,
                                 null=True,
                                 blank=True)
    video_to_renewal = ArrayField(models.CharField(max_length=20),
                                  default=list,
                                  null=True,
                                  blank=True)

    def __str__(self):
        return self.authority