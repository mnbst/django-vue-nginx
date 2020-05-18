from rest_framework import serializers

from .models import Video


class VideoSerializer(serializers.ModelSerializer):
    videoHref = serializers.CharField(source='video_href')
    videoImg = serializers.CharField(source='video_img')
    videoTime = serializers.CharField(source='video_time')
    videoTitle = serializers.CharField(source='video_title')
    videoGenre = serializers.ListField(child=serializers.CharField(), source='video_genre')
    publishedAt = serializers.CharField(source='published_at')

    class Meta:
        model = Video
        fields = ('videoHref', 'videoImg', 'videoTime', 'videoTitle', 'videoGenre', 'publishedAt', 'want', 'excepted')
