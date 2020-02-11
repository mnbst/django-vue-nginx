from rest_framework import viewsets
from .models import Word
from .models import Caption
from .models import Video
from .models import FetchSetting
from .serializers import WordSerializer
from .serializers import CaptionSerializer
from .serializers import VideoSerializer
from .serializers import FetchSettingSerializer


class WordView(viewsets.ModelViewSet):
    queryset = Word.objects.all()
    serializer_class = WordSerializer


class CaptionView(viewsets.ModelViewSet):
    queryset = Caption.objects.all()
    serializer_class = CaptionSerializer


class VideoView(viewsets.ModelViewSet):
    queryset = Video.objects.all()
    serializer_class = VideoSerializer


class FetchSettingView(viewsets.ModelViewSet):
    queryset = FetchSetting.objects.all()
    serializer_class = FetchSettingSerializer
