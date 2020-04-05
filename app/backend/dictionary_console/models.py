from __future__ import absolute_import

from django.contrib.postgres.fields import ArrayField
from django.core.validators import MaxValueValidator
from django.db import models


class Word(models.Model):
    word_ini = models.CharField(max_length=1, db_index=True)
    word = models.CharField(max_length=50, unique=True)
    meaning = models.CharField(max_length=200, default='')

    def __str__(self):
        return self.word


class Video(models.Model):
    video_href = models.CharField(max_length=20, unique=True)
    video_img = models.CharField(max_length=100)
    video_time = models.CharField(max_length=10)
    video_title = models.CharField(max_length=100)
    video_genre = ArrayField(models.CharField(max_length=50))
    youtubeID = models.CharField(max_length=50)
    video_upload_date = models.DateTimeField()

    def __str__(self):
        return self.video_href


class Caption(models.Model):
    index = models.PositiveIntegerField(default=0)
    start_time = models.PositiveIntegerField(default=0, validators=[MaxValueValidator(9999999999)])
    end_time = models.PositiveIntegerField(default=0, validators=[MaxValueValidator(9999999999)])
    text = models.CharField(max_length=500)
    words = ArrayField(models.CharField(max_length=20, null=True, blank=True))
    meanings = ArrayField(
        models.CharField(max_length=200, null=True, blank=True))
    video_href = models.ForeignKey(Video, to_field='video_href', on_delete=models.CASCADE)

    def __str__(self):
        return str(self.text)


class WordAppearance(models.Model):
    word = models.ForeignKey(Word, to_field='word', on_delete=models.CASCADE)
    video_href = models.ForeignKey(Video, to_field='video_href', on_delete=models.CASCADE)
    appearance = ArrayField(models.IntegerField(default=0))

    @classmethod
    def convert_objects(cls, word: str):
        word_appearances = cls.objects.filter(word=word)
        return list(map(lambda x: {x.video_href: x.appearance}, word_appearances))

    def __str__(self):
        return self.word


class FetchSetting(models.Model):
    authority = models.CharField(max_length=30, default="super",
                                 blank=True, unique=True)
    excepted_href = ArrayField(models.CharField(max_length=20),
                               default=list,
                               null=True,
                               blank=True)
    page_to_crawl = models.PositiveIntegerField(default=5)
    language_limit = models.PositiveIntegerField(default=1)
    minimum_sentence = models.PositiveIntegerField(default=10)
    video_per_page = models.PositiveIntegerField(default=10)
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
