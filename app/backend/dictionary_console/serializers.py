from rest_framework import serializers
from .models import *


class WordSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Word
        fields = ('id', 'url', 'word_ini', 'word', 'meaning')


class WordAppearanceSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = WordAppearance
        fields = ('id', 'url', 'word_id', 'appearance')


class CaptionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Caption
        fields = ('id', 'url', 'video_href', 'index', 'start_time', 'end_time',
                  'text', 'word', 'word_imi')


class VideoSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Video
        fields = ('id', 'url', 'video_href', 'video_title', 'video_img',
                  'video_time', 'video_genre', 'youtubeID',
                  'video_upload_date')


class FetchSettingSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = FetchSetting
        fields = ('id', 'url', 'authority', 'excepted_href', 'page_to_crawl',
                  'language_limit', 'minimum_sentence', 'video_to_delete',
                  'video_to_renewal', 'video_per_page')
