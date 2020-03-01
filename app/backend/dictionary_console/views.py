from rest_framework import viewsets
from .serializers import *


class WordView(viewsets.ModelViewSet):
    queryset = Word.objects.all()
    serializer_class = WordSerializer


class WordAppearanceView(viewsets.ModelViewSet):
    queryset = WordAppearance.objects.all()
    serializer_class = WordAppearanceSerializer


class CaptionView(viewsets.ModelViewSet):
    queryset = Caption.objects.all()
    serializer_class = CaptionSerializer


class VideoView(viewsets.ModelViewSet):
    queryset = Video.objects.all()
    serializer_class = VideoSerializer


class FetchSettingView(viewsets.ModelViewSet):
    queryset = FetchSetting.objects.all()
    serializer_class = FetchSettingSerializer
