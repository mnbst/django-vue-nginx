from __future__ import absolute_import

from django.contrib.postgres.fields import ArrayField
from django.core.validators import MaxValueValidator
from django.db import models


class Word(models.Model):
    word_ini = models.CharField(max_length=1, db_index=True)
    word = models.CharField(max_length=50, unique=True)
    meaning = models.CharField(max_length=200, default='')
    ng = models.BooleanField(default=False)

    class Meta:
        ordering = ["word"]

    def __str__(self):
        return self.word


class Video(models.Model):
    video_href = models.CharField(max_length=20, unique=True)
    video_img = models.CharField(max_length=100)
    video_time = models.CharField(max_length=10)
    video_title = models.CharField(max_length=100)
    video_genre = ArrayField(models.CharField(max_length=50))
    youtubeID = models.CharField(max_length=50)
    published_at = models.CharField(max_length=50, default='')
    want = models.BooleanField(default=True)
    excepted = models.BooleanField(default=False)

    class Meta:
        ordering = ["-published_at"]

    def __str__(self):
        return self.video_href


# class WordAppearance(models.Model):
#     word = models.ForeignKey(Word, to_field='id', on_delete=models.CASCADE, db_index=True)
#     video_caption = models.ForeignKey(Video, to_field='id', on_delete=models.CASCADE, db_index=True)
#     appearance = ArrayField(models.CharField(max_length=10))
#
#     def convert_objects(self):
#         word_appearances = self.objects.filter(word=self.word)
#         return list(map(lambda x: {x.video_href: x.appearance}, word_appearances))
#
#     def __str__(self):
#         return self.word


class Caption(models.Model):
    index = models.PositiveIntegerField(default=0)
    start_time = models.PositiveIntegerField(default=0, validators=[MaxValueValidator(9999999999)])
    end_time = models.PositiveIntegerField(default=0, validators=[MaxValueValidator(9999999999)])
    text = models.CharField(max_length=255)
    video = models.ForeignKey(Video, on_delete=models.CASCADE, db_index=True, null=True)
    words = models.ManyToManyField(Word, through='CaptionWord', blank=True)

    class Meta:
        ordering = ["index"]

    def __str__(self):
        return str(self.text)


class CaptionWord(models.Model):
    caption = models.ForeignKey(Caption, on_delete=models.CASCADE)
    word = models.ForeignKey(Word, on_delete=models.CASCADE)
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return str(self)


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
