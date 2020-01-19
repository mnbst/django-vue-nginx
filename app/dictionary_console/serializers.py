from rest_framework import serializers
from .models import Word
from .models import Video
from .models import Caption
from .models import VideoExcepted


class WordSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Word
        fields = ('id', 'url', 'word_ini', 'word', 'word_imi')


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
class VideoExceptedSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = VideoExcepted
        fields = ('id', 'url', 'video_href', 'video_title', 'video_img')
